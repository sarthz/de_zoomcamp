# -*- coding: utf-8 -*- #
# Copyright 2022 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Command for migrate from legacy firewall rules to network firewall policies."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import json
import re

from googlecloudsdk.api_lib.compute import base_classes
from googlecloudsdk.api_lib.compute.operations import poller
from googlecloudsdk.api_lib.util import waiter
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.compute import flags as compute_flags
from googlecloudsdk.command_lib.compute.networks import flags as network_flags
from googlecloudsdk.core import log
from googlecloudsdk.core import properties
from googlecloudsdk.core.util import files


def _GetFirewallPoliciesAssociatedWithNetwork(network, firewall_policies):
  filtered_policies = []
  for firewall_policy in firewall_policies:
    associated = False
    for association in firewall_policy.associations:
      if association.attachmentTarget == network.selfLink:
        associated = True
    if associated:
      filtered_policies.append(firewall_policy)
  return filtered_policies


def _GetFirewallsAssociatedWithNetwork(network, firewalls):
  filtered_firewalls = []
  for firewall in firewalls:
    if firewall.network == network.selfLink:
      filtered_firewalls.append(firewall)
  return filtered_firewalls


def _GetLegacyTags(firewalls):
  tags = set()
  for firewall in firewalls:
    tags.update(firewall.sourceTags)
    tags.update(firewall.targetTags)
  return tags


def _IsDefaultFirewallPolicyRule(rule):
  # Default egress/ingress IPv4/IPv6 rules
  if 2147483644 <= rule.priority <= 2147483647:
    return True
  # Probably a user defined rule
  return False


def _UnsupportedTagResult(field, tag):
  return (False, 'Mapping for {} \'{}\' was not found.'.format(field, tag))


def _IsFirewallSupported(firewall, tag_mapping, disable_logging):
  """Checks if the given VPC Firewall can be converted by the Migration Tool."""
  # Source Service Accounts
  if firewall.sourceServiceAccounts:
    return (False, 'Firewalls with source_service_accounts are not supported.')
  # Source Tags
  for tag in firewall.sourceTags:
    if tag not in tag_mapping:
      return _UnsupportedTagResult('source_tag', tag)
  # Target Tags
  for tag in firewall.targetTags:
    if tag not in tag_mapping:
      return _UnsupportedTagResult('target_tag', tag)
  # Logging is not supported in Network Firewall Policies MVP
  if not disable_logging and firewall.logConfig and firewall.logConfig.enable:
    return (False, 'Logging is not supported in Network Firewall Policy MVP.')
  return (True, '')


def _IsGkeFirewall(firewall):
  return re.match(r'gke-(.*)-(.*)', firewall.name)


def _IsCustomerDefinedFirewall(firewall):
  return not _IsGkeFirewall(firewall)


def _ConvertRuleDirection(messages, direction):
  if direction == messages.Firewall.DirectionValueValuesEnum.INGRESS:
    return messages.FirewallPolicyRule.DirectionValueValuesEnum.INGRESS
  return messages.FirewallPolicyRule.DirectionValueValuesEnum.EGRESS


def _ConvertLayer4Configs(messages, l4_configs):
  layer4_configs = []
  for config in l4_configs:
    layer4_configs.append(
        messages.FirewallPolicyRuleMatcherLayer4Config(
            ipProtocol=config.IPProtocol, ports=config.ports))
  return layer4_configs


def _ConvertTags(messages, tag_mapping, tags):
  return [
      messages.FirewallPolicyRuleSecureTag(name=tag_mapping[tag])
      for tag in tags
  ]


def _ConvertRuleInternal(messages, firewall, action, l4_configs, tag_mapping,
                         disable_logging):
  return messages.FirewallPolicyRule(
      disabled=firewall.disabled,
      ruleName=firewall.name,  # Allow and deny cannot be in the same rule
      description=firewall.description,  # Do not change description
      direction=_ConvertRuleDirection(messages, firewall.direction),
      priority=firewall.priority,
      action=action,
      enableLogging=(not disable_logging and firewall.logConfig.enable),
      match=messages.FirewallPolicyRuleMatcher(
          destIpRanges=firewall.destinationRanges,
          srcIpRanges=firewall.sourceRanges,
          srcSecureTags=_ConvertTags(messages, tag_mapping,
                                     firewall.sourceTags),
          layer4Configs=_ConvertLayer4Configs(messages, l4_configs)),
      targetSecureTags=_ConvertTags(messages, tag_mapping, firewall.targetTags),
      targetServiceAccounts=firewall.targetServiceAccounts)


def _ConvertRule(messages, firewall, tag_mapping, disable_logging):
  if firewall.denied:
    return _ConvertRuleInternal(messages, firewall, 'deny', firewall.denied,
                                tag_mapping, disable_logging)
  return _ConvertRuleInternal(messages, firewall, 'allow', firewall.allowed,
                              tag_mapping, disable_logging)


def _IsPrefixTrue(statuses):
  false_detected = False
  for status in statuses:
    if status and false_detected:
      return False
    false_detected = false_detected or not status
  return True


def _IsSuffixTrue(statuses):
  statuses_copy = statuses
  statuses_copy.reverse()
  return _IsPrefixTrue(statuses_copy)


def _ReadTagMapping(file_name):
  """Imports legacy to secure tag mapping from a JSON file."""
  try:
    with files.FileReader(file_name) as f:
      data = json.load(f)
  except FileNotFoundError:
    log.status.Print(
        'File \'{file}\' was not found. Tag mapping was not imported.'.format(
            file=file_name))
    return None
  except OSError:
    log.status.Print(
        'OS error occurred when opening the file \'{file}\'. Tag mapping was not imported.'
        .format(file=file_name))
    return None
  except Exception as e:  # pylint: disable=broad-except
    log.status.Print(
        'Unexpected error occurred when reading the JSON file \'{file}\'. Tag mapping was not imported.'
        .format(file=file_name))
    log.status.Print(repr(e))
    return None

  return data


def _WriteTagMapping(file_name, tags):
  """Exports legacy to secure tag mapping to a JSON file."""
  mapping = dict.fromkeys(tags)

  try:
    with files.FileWriter(path=file_name, create_path=True) as f:
      json.dump(mapping, f)
  except OSError:
    log.status.Print(
        'OS error occurred when opening the file \'{file}\'. Tag mapping was not exported.'
        .format(file=file_name))
    return
  except Exception as e:  # pylint: disable=broad-except
    log.status.Print(
        'Unexpected error occurred when writing the JSON file \'{file}\'. Tag mapping was not exported.'
        .format(file=file_name))
    log.status.Print(repr(e))


@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class MigrateAlpha(base.CreateCommand):
  """Migrate from legacy firewall rules to network firewall policies."""

  NETWORK_ARG = None

  @classmethod
  def Args(cls, parser):
    # required --target-firewall-policy=TARGET_FIREWALL_POLICY argument
    group = parser.add_group(mutex=True, required=True)
    group.add_argument(
        '--target-firewall-policy',
        help="""\
      Name of the new Network Firewall Policy used to store the migration
      result.
      """)
    group.add_argument(
        '--export-tag-mapping',
        action='store_true',
        help="""\
      If set, migration tool will inspect all VPC Firewalls attached to
      SOURCE_NETWORK, collect all source and target tags, and store them in
      TAG_MAPPING_FILE.
      """)
    # required --source-network=NETWORK flag
    cls.NETWORK_ARG = compute_flags.ResourceArgument(
        name='--source-network',
        resource_name='network',
        completer=network_flags.NetworksCompleter,
        plural=False,
        required=True,
        global_collection='compute.networks',
        short_help='The VPC Network for which the migration should be performed.',
        detailed_help=None)
    cls.NETWORK_ARG.AddArgument(parser)
    # optional --tag-mapping-file=TAG_MAPPING_FILE argument
    parser.add_argument(
        '--tag-mapping-file',
        required=False,
        help='Path to a JSON file with legacy to secure tag mapping.')
    # optional --disable-logging argument
    parser.add_argument(
        '--disable-logging',
        action='store_true',
        required=False,
        help="""\
      If set, migration tool will not migrate logging config. This is a
      workaround to use before Network Firewall Policies support logging.
      """)

  def Run(self, args):
    """Run the migration logic."""
    holder = base_classes.ComputeApiHolder(self.ReleaseTrack())
    client = holder.client.apitools_client
    messages = client.MESSAGES_MODULE

    # Determine project
    if args.project:
      project = args.project
    else:
      project = properties.VALUES.core.project.GetOrFail()

    # Get Input Parameters
    network_name = getattr(args, 'source_network')
    policy_name = getattr(args, 'target_firewall_policy', None)
    export_tag_mapping = getattr(args, 'export_tag_mapping', False)
    tag_mapping_file_name = getattr(args, 'tag_mapping_file', None)
    disable_logging = getattr(args, 'disable_logging', False)

    # In the export tag mode, the tag mapping file must be provided
    if export_tag_mapping and not tag_mapping_file_name:
      raise Exception(
          '--tag-mapping-file must be specified if --export-tag-mapping is set.'
      )

    # Get VPC Network
    network = client.networks.Get(
        messages.ComputeNetworksGetRequest(
            project=project, network=network_name))

    log.status.Print(
        'Looking for VPC Firewalls and Network Firewall Policies associated with VPC Network \'{}\'.'
        .format(network_name))

    # Get all Firewall Policies
    response = client.networkFirewallPolicies.List(
        messages.ComputeNetworkFirewallPoliciesListRequest(project=project))

    # Verify there is no Firewall Policy with provided name
    for firewall_policy in response.items:
      if firewall_policy.name == policy_name:
        log.status.Print('Firewall Policy "' + policy_name +
                         '" already exists.')
        return

    # Filter Network Firewall Policies attached to the given VPC Network
    firewall_policies = _GetFirewallPoliciesAssociatedWithNetwork(
        network, response.items)
    log.status.Print(
        'Found {} Network Firewall Policies associated with the VPC Network \'{}\'.'
        .format(len(firewall_policies), network_name))

    # Migration tool does not support multiple FirewallPolicies.
    if len(firewall_policies) > 1:
      log.status.Print(
          'Migration tool does not support multiple Network Firewall Policies '
          'associated with a single VPC Network.')
      return

    # List all legacy VPC Firewalls attached to the given VPC Network
    # Hidden VPC Firewalls are not listed.
    # TODO(b/222646415) Support more than 500 VPC Firewalls (maxResults)!
    response = client.firewalls.List(
        messages.ComputeFirewallsListRequest(project=project))
    firewalls = _GetFirewallsAssociatedWithNetwork(network, response.items)
    log.status.Print(
        'Found {} VPC Firewalls associated with the VPC Network \'{}\'.\n'
        .format(len(firewalls), network_name))

    # Now we fetched all VPC Firewalls and Firewall Policies attached to the
    # given VPC Network.

    # Branch 1: Just generate pre-mapping for legacy tags
    if export_tag_mapping:
      legacy_tags = _GetLegacyTags(firewalls)
      _WriteTagMapping(tag_mapping_file_name, legacy_tags)
      log.status.Print(
          'Legacy tags were exported to \'{}\''.format(tag_mapping_file_name))
      return

    # Branch 2: Do the actual migration

    # Read tag mapping if provided
    tag_mapping = dict()
    if tag_mapping_file_name:
      tag_mapping = _ReadTagMapping(tag_mapping_file_name)
      if not tag_mapping:
        return

    # Sort VPC Firewalls by priorities. If two Firewalls have the same priority
    # then deny rules should precede allow rules. Third coordinate is unique to
    # avoid comparison between Firewall objects which is undefined.

    # Add unique ID to each firewall
    firewalls_temp = []
    firewalls_counter = 0
    for firewall in firewalls:
      firewalls_temp.append((firewalls_counter, firewall))
      firewalls_counter = firewalls_counter + 1
    # Build tuple
    firewalls = [
        (f.priority, 0 if f.denied else 1, id, f) for (id, f) in firewalls_temp
    ]
    firewalls = sorted(firewalls)

    # Convert user provided VPC Firewalls if possible
    converted_firewalls = []
    conversion_failures = 0
    customer_defined_firewalls = 0
    for (priority, _, _, firewall) in firewalls:
      (status, error) = (False, 'Not a customer defined VPC Firewall.')
      converted_firewall = None
      is_custom = _IsCustomerDefinedFirewall(firewall)
      # Convert only supported customer defined VPC Firewalls
      if is_custom:
        customer_defined_firewalls = customer_defined_firewalls + 1
        (status, error) = _IsFirewallSupported(firewall, tag_mapping,
                                               disable_logging)
        if status:
          converted_firewall = _ConvertRule(messages, firewall, tag_mapping,
                                            disable_logging)
        else:
          conversion_failures = conversion_failures + 1
      converted_firewalls.append(
          (priority, firewall, is_custom, converted_firewall, status, error))

    # Print info about detected customer defined VPC Firewalls.
    log.status.Print('Found {} customer defined VPC Firewalls.'.format(
        customer_defined_firewalls))
    log.status.Print('priority: name \'description\'')
    for (_, firewall, is_custom, _, _, _) in converted_firewalls:
      if is_custom:
        log.status.Print('{}: {} \'{}\''.format(firewall.priority,
                                                firewall.name,
                                                firewall.description))
    log.status.Print('')

    # Print info about conversion failures
    if conversion_failures:
      log.status.Print(
          'Could not convert {} VPC Firewalls:'.format(conversion_failures))
      for (_, firewall, _, _, status, error) in converted_firewalls:
        if not status:
          log.status.Print('{}: {} - {}'.format(firewall.priority,
                                                firewall.name, error))
      log.status.Print('')

    # Filter out default FirewallPolicy.Rules
    # There is at most one firewall policy to iterate on.
    firewall_policy_rules = []
    for firewall_policy in firewall_policies:
      for rule in firewall_policy.rules:
        if not _IsDefaultFirewallPolicyRule(rule):
          firewall_policy_rules.append(rule)

    # Sort FirewallPolicy.Rules by priority
    firewall_policy_rules = [
        (rule.priority, rule) for rule in firewall_policy_rules
    ]
    firewall_policy_rules = sorted(firewall_policy_rules)

    # Adjust the format to match list of converted VPC Firewalls
    firewall_policy_rules = [(priority, None, True, rule, True, '')
                             for (priority, rule) in firewall_policy_rules]

    # Join converted VPC Firewalls with Network Firewall Policy Rules
    joined_rules = []
    if network.networkFirewallPolicyEnforcementOrder == messages.Network.NetworkFirewallPolicyEnforcementOrderValueValuesEnum.AFTER_CLASSIC_FIREWALL:
      joined_rules.extend(converted_firewalls)
      joined_rules.extend(firewall_policy_rules)
    else:
      joined_rules.extend(firewall_policy_rules)
      joined_rules.extend(converted_firewalls)

    # Check if extraction of selected rules is possible
    # Extracted rules must be a prefix for BEFORE_CLASSIC_FIREWALL mode and
    # suffix for AFTER_CLASSIC_FIREWALL mode.
    statuses = [status for (_, _, _, _, status, _) in joined_rules]
    if network.networkFirewallPolicyEnforcementOrder == messages.Network.NetworkFirewallPolicyEnforcementOrderValueValuesEnum.AFTER_CLASSIC_FIREWALL:
      if not _IsSuffixTrue(statuses):
        log.status.Print(
            'Migration is impossible, because rule evaluation order cannot be preserved.'
        )
        return
    else:
      if not _IsPrefixTrue(statuses):
        log.status.Print(
            'Migration is impossible, because rule evaluation order cannot be preserved.'
        )
        return

    # Extract rules to migrate
    rules_to_migrate = [(p, r, f) for (p, f, _, r, s, _) in joined_rules if s]

    # Check if priorities remap is needed
    priorities_remap_needed = (
        len(set([p for (p, r, f) in rules_to_migrate])) !=
        len(rules_to_migrate))

    # Compute new priorities if needed
    if priorities_remap_needed:
      log.status.Print('Updating rules priorities to avoid collisions.')
      log.status.Print(
          'new-priority: old-priority rule-name \'rule-description\'')

    current_priority = 1000
    migrated_rules = []
    for (priority, rule, firewall) in rules_to_migrate:
      if priorities_remap_needed:
        rule.priority = current_priority
        current_priority = current_priority + 1
        log.status.Print('{}: {} {} \'{}\''.format(rule.priority, priority,
                                                   rule.ruleName,
                                                   rule.description))
      migrated_rules.append((rule, firewall))
    if priorities_remap_needed:
      log.status.Print('')

    # Create a new Network Firewall Policy
    firewall_policy = messages.FirewallPolicy(
        description='Network Firewall Policy containing all VPC Firewalls and FirewallPolicy.Rules migrated using GCP Firewall Migration Tool.',
        name=policy_name,
        vpcNetworkScope=messages.FirewallPolicy.VpcNetworkScopeValueValuesEnum
        .GLOBAL_VPC_NETWORK)
    response = client.networkFirewallPolicies.Insert(
        messages.ComputeNetworkFirewallPoliciesInsertRequest(
            project=project, firewallPolicy=firewall_policy))
    # Wait until Network Firewall Policy is created
    operation_poller = poller.Poller(client.networkFirewallPolicies)
    operation_ref = holder.resources.Parse(
        response.selfLink, collection='compute.globalOperations')
    waiter.WaitFor(
        operation_poller, operation_ref,
        'Creating new Network Firewall Policy \'{}\''.format(policy_name))

    # Add migrated rules to newly created policy
    log.status.Print('Successfully migrated the following VPC Firewalls:')
    log.status.Print('old-priority: rule-name \'rule-description\'')
    for (rule, firewall) in migrated_rules:
      client.networkFirewallPolicies.AddRule(
          messages.ComputeNetworkFirewallPoliciesAddRuleRequest(
              firewallPolicy=policy_name,
              firewallPolicyRule=rule,
              project=project))
      if firewall:
        log.status.Print('{}: {} \'{}\''.format(firewall.priority,
                                                firewall.name,
                                                firewall.description))


MigrateAlpha.detailed_help = {
    'brief':
        'Create a new Network Firewall Policy and move all customer defined '
        'firewall rules there.',
    'DESCRIPTION':
        """
*{command}* is used to create a new Network Firewall Policy that contain
all rules defined in already existing Network Firewall Policy associated with
the given VPC Network and all customer defined VPC Firewall Rules attached to
that VPC Network.
""",
    'EXAMPLES':
        """
To execute the migration for VPC Network 'my-network' which stores the result
in 'my-policy' Network Firewall Policy, run:

  $ {command} --source-network=my-network --target-firewall-policy=my-policy
  """,
}
