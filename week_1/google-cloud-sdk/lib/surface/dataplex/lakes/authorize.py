# -*- coding: utf-8 -*- #
# Copyright 2022 Google Inc. All Rights Reserved.
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
"""Command to authorize a P4SA service account to another resource."""


from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.cloudresourcemanager import projects_api
from googlecloudsdk.api_lib.dataplex import lake
from googlecloudsdk.api_lib.storage import storage_api
from googlecloudsdk.api_lib.storage import storage_util
from googlecloudsdk.api_lib.util import apis
from googlecloudsdk.api_lib.util import exceptions as gcloud_exception
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.dataplex import resource_args
from googlecloudsdk.command_lib.projects import util as project_util


@base.ReleaseTracks(base.ReleaseTrack.ALPHA, base.ReleaseTrack.GA)
class Authorize(base.Command):
  """Authorize a project service account to manage given resource.

  IAM Bindings for the service account of the primary project will be added to
  a secondary project, a storage bucket, or BigQuery dataset.
  """

  detailed_help = {
      'EXAMPLES':
          """\
          To authorize the service account in project `test-project` to
          manage another project `test-project2`, run:

            $ {command} --project=test-project --project-resource=test-project2

          To authorize the service account in project `test-project` to
          manage the storage bucket `dataplex-storage-bucket`, run:

            $ {command} --project=test-project --storage-bucket-resource=dataplex-storage-bucket

          To authorize the service account in project `test-project` to
          manage the BigQuery dataset `test-dataset` in project `test-project2`,
          run:

            $ {command} --project=test-project --bigquery-dataset-resource=test-dataset --secondary-project=test-project2
          """,
  }

  @staticmethod
  def Args(parser):
    resource_args.AddProjectArg(parser,
                                'to add service agent IAM policy binding to.')
    data_group = parser.add_group(
        mutex=True, required=True, help='Container or Object to bind P4SA.')
    data_group.add_argument(
        '--storage-bucket-resource',
        help="""The identifier of the Cloud Storage bucket to authorize the
                project on.""")
    data_group.add_argument(
        '--project-resource',
        help='The identifier of the project to authorize.')
    dataset_group = data_group.add_group(
        help='Fields to help identify the BigQuery Dataset.')
    dataset_group.add_argument(
        '--bigquery-dataset-resource',
        required=True,
        help='The identifier of the BigQuery dataset to authorize.'
    )
    dataset_group.add_argument(
        '--secondary-project',
        required=True,
        help='The identifier of the Project where BigQuery dataset resides.')

  @gcloud_exception.CatchHTTPErrorRaiseHTTPException(
      'Status code: {status_code}. {status_message}.')
  def Run(self, args):
    project_ref = args.CONCEPTS.project.Parse()
    service_account = 'service-' + str(
        project_util.GetProjectNumber(project_ref.projectsId)
    ) + '@gcp-sa-dataplex.iam.gserviceaccount.com'

    if args.IsSpecified('storage_bucket_resource'):
      return storage_api.StorageClient().AddIamPolicyBinding(
          storage_util.BucketReference(args.storage_bucket_resource),
          'serviceAccount:' + service_account, 'roles/dataplex.serviceAgent')

    if args.IsSpecified('bigquery_dataset_resource'):
      get_dataset_request = apis.GetMessagesModule(
          'bigquery', 'v2').BigqueryDatasetsGetRequest(
              datasetId=args.bigquery_dataset_resource,
              projectId=args.secondary_project)
      dataset = apis.GetClientInstance(
          'bigquery', 'v2').datasets.Get(request=get_dataset_request)
      lake.AddServiceAccountToDatasetPolicy(
          apis.GetMessagesModule('bigquery', 'v2').Dataset.AccessValueListEntry,
          dataset, service_account, 'roles/dataplex.serviceAgent')
      return apis.GetClientInstance('bigquery', 'v2').datasets.Patch(
          apis.GetMessagesModule('bigquery', 'v2').BigqueryDatasetsPatchRequest(
              datasetId=args.bigquery_dataset_resource,
              projectId=args.secondary_project,
              dataset=dataset))

    if args.IsSpecified('project_resource'):
      return projects_api.AddIamPolicyBinding(
          project_util.ParseProject(args.project_resource),
          'serviceAccount:' + service_account, 'roles/dataplex.serviceAgent')
