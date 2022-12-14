# -*- coding: utf-8 -*- #
# Copyright 2015 Google LLC. All Rights Reserved.
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
"""gcloud datastore emulator start command."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import socket
from googlecloudsdk.calliope import arg_parsers
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.emulators import firestore_util
from googlecloudsdk.command_lib.emulators import util
from googlecloudsdk.command_lib.util import java
from googlecloudsdk.core import log


@base.ReleaseTracks(base.ReleaseTrack.ALPHA, base.ReleaseTrack.BETA)
class Start(base.Command):
  """Start a local firestore emulator.

  This command starts a local firestore emulator.
  """

  detailed_help = {
      'EXAMPLES':
          """\
          To start a local firestore emulator, run:

            $ {command}
          """,
  }

  @staticmethod
  def Args(parser):
    parser.add_argument(
        '--rules',
        required=False,
        help='If set, all projects will use the security rules in this file')
    parser.add_argument(
        '--host-port',
        required=False,
        type=lambda arg: arg_parsers.HostPort.Parse(arg, ipv6_enabled=True),
        help='The host:port to which the emulator should be bound. Can '
        'take the form of a single address (hostname, IPv4, or IPv6) and/or '
        'port:\n\n  [ADDRESS][:PORT]\n\n'
        'In this format you must enclose IPv6 addresses in square brackets: '
        'e.g.\n\n'
        '  [2001:db8:0:0:0:ff00:42:8329]:8080\n\n'
        'The default value is localhost:8080.')

  # TODO(b/221477106): Remove this warning after b/221477106 is fixed.
  def LogJavaVersionWarning(self):
    """Log a warning message notifying users about Java version change.

    Log the warning when the installed JRE has an earlier version than Java 11.
    """
    try:
      java.RequireJavaInstalled(firestore_util.FIRESTORE_TITLE, min_version=11)
    except java.JavaVersionError:
      log.warning(
          'Cloud Firestore Emulator support for Java JRE version 8 will be '
          'dropped after gcloud command-line tool release 392.0.0. Please '
          'upgrade to Java JRE version 11 or higher to continue using the '
          'latest Cloud Firestore Emulator.')
    except java.JavaError:
      # A JRE could not be found. Not logging the warning since the user will
      # not be able to start an emulator anyways.
      pass

  def Run(self, args):
    if not args.host_port:
      args.host_port = arg_parsers.HostPort.Parse(
          firestore_util.GetHostPort(), ipv6_enabled=socket.has_ipv6)
    args.host_port.host = args.host_port.host or 'localhost'
    args.host_port.port = args.host_port.port or '8080'
    firestore_util.ValidateStartArgs(args)
    self.LogJavaVersionWarning()
    with firestore_util.StartFirestoreEmulator(args) as proc:
      util.PrefixOutput(proc, 'firestore')
