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
"""Hooks for beyondCorp client connector service commands."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import json
from googlecloudsdk.api_lib.beyondcorp.app import util as api_util
from googlecloudsdk.api_lib.util import messages as messages_util
from googlecloudsdk.core import exceptions
from googlecloudsdk.core.util import files


def ParseConfig(unused_ref, args, request):
  """Parse client connector service config."""
  if args.IsSpecified('config_from_file'):
    path = args.config_from_file
    try:
      content_file = files.ReadFileContents(path)
    except files.Error as e:
      raise exceptions.Error(
          'Specified config file path is invalid:\n{}'.format(e))
    data = json.loads(content_file)
    display_name = data['displayName'] if 'displayName' in data else None
    return ConstructRequest(data['ingress']['config'],
                            data['egress']['peeredVpc'],
                            display_name, args, request)
  elif args.IsSpecified('ingress_config') and args.IsSpecified(
      'egress_peered_vpc'):
    return ConstructRequest(
        json.loads(args.ingress_config), json.loads(args.egress_peered_vpc),
        args.display_name, args, request)
  else:
    raise exceptions.Error('Incorrect arguments provided. Try --help.')


def ConstructRequest(ingress_config, egress_vpc, display_name, args, request):
  """Construct request from the given client connector service config."""
  messages = api_util.GetMessagesModule(args.calliope_command.ReleaseTrack())
  if request.clientConnectorService is None:
    request.clientConnectorService = messages.ClientConnectorService()
  if request.clientConnectorService.ingress is None:
    request.clientConnectorService.ingress = messages.Ingress()
  if request.clientConnectorService.ingress.config is None:
    request.clientConnectorService.ingress.config = messages_util.DictToMessageWithErrorCheck(
        ingress_config, messages.Config)
  if request.clientConnectorService.egress is None:
    request.clientConnectorService.egress = messages.Egress()
  if request.clientConnectorService.egress.peeredVpc is None:
    request.clientConnectorService.egress.peeredVpc = messages_util.DictToMessageWithErrorCheck(
        egress_vpc, messages.PeeredVpc)
  if args.IsSpecified('display_name') or display_name is not None:
    request.clientConnectorService.displayName = display_name
  return request


def CheckUpdateFieldsSpecified(unused_ref, args, patch_request):
  """Check that update command has one of these flags specified."""
  update_args = [
      'display_name',
  ]
  if any(args.IsSpecified(update_arg) for update_arg in update_args):
    return patch_request
  raise exceptions.Error(
      'Must specify at least one field to update. Try --help.')
