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
"""Flags for VMware Engine network policies commands."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.calliope.concepts import concepts
from googlecloudsdk.command_lib.util.apis import yaml_data
from googlecloudsdk.command_lib.util.concepts import concept_parsers
from googlecloudsdk.command_lib.util.concepts import presentation_specs


def AddNetworkPolicyToParser(parser, positional=False):
  """Sets up an argument for the VMware Engine network policy resource."""
  name = '--network-policy'
  if positional:
    name = 'network_policy'
  network_policy_data = yaml_data.ResourceYAMLData.FromPath(
      'vmware.network_policies.network_policy')
  resource_spec = concepts.ResourceSpec.FromYaml(network_policy_data.GetData())
  if positional:
    presentation_spec = presentation_specs.ResourcePresentationSpec(
        name=name,
        concept_spec=resource_spec,
        required=True,
        group_help='network_policy.')
  else:
    presentation_spec = presentation_specs.ResourcePresentationSpec(
        name=name,
        concept_spec=resource_spec,
        required=True,
        group_help='network_policy.',
        flag_name_overrides={'location': '--network-policy-location'})
  return concept_parsers.ConceptParser([presentation_spec]).AddToParser(parser)


def AddLocationArgToParser(parser, positional=False):
  """Parses location flag."""
  location_data = yaml_data.ResourceYAMLData.FromPath(
      'vmware.network_policies.location')
  resource_spec = concepts.ResourceSpec.FromYaml(location_data.GetData())
  name = '--location'
  if positional:
    name = 'location'
  presentation_spec = presentation_specs.ResourcePresentationSpec(
      name=name,
      concept_spec=resource_spec,
      required=True,
      group_help='location.')
  return concept_parsers.ConceptParser([presentation_spec]).AddToParser(parser)
