"""Generated client library for translate version v3beta1."""
# NOTE: This file is autogenerated and should not be edited by hand.

from __future__ import absolute_import

from apitools.base.py import base_api
from googlecloudsdk.third_party.apis.translate.v3beta1 import translate_v3beta1_messages as messages


class TranslateV3beta1(base_api.BaseApiClient):
  """Generated client library for service translate version v3beta1."""

  MESSAGES_MODULE = messages
  BASE_URL = 'https://translation.googleapis.com/'
  MTLS_BASE_URL = 'https://translation.mtls.googleapis.com/'

  _PACKAGE = 'translate'
  _SCOPES = ['https://www.googleapis.com/auth/cloud-platform', 'https://www.googleapis.com/auth/cloud-translation']
  _VERSION = 'v3beta1'
  _CLIENT_ID = '1042881264118.apps.googleusercontent.com'
  _CLIENT_SECRET = 'x_Tw5K8nnjoRAqULM9PFAC2b'
  _USER_AGENT = 'google-cloud-sdk'
  _CLIENT_CLASS_NAME = 'TranslateV3beta1'
  _URL_VERSION = 'v3beta1'
  _API_KEY = None

  def __init__(self, url='', credentials=None,
               get_credentials=True, http=None, model=None,
               log_request=False, log_response=False,
               credentials_args=None, default_global_params=None,
               additional_http_headers=None, response_encoding=None):
    """Create a new translate handle."""
    url = url or self.BASE_URL
    super(TranslateV3beta1, self).__init__(
        url, credentials=credentials,
        get_credentials=get_credentials, http=http, model=model,
        log_request=log_request, log_response=log_response,
        credentials_args=credentials_args,
        default_global_params=default_global_params,
        additional_http_headers=additional_http_headers,
        response_encoding=response_encoding)
    self.projects_locations_glossaries = self.ProjectsLocationsGlossariesService(self)
    self.projects_locations_operations = self.ProjectsLocationsOperationsService(self)
    self.projects_locations = self.ProjectsLocationsService(self)
    self.projects = self.ProjectsService(self)

  class ProjectsLocationsGlossariesService(base_api.BaseApiService):
    """Service class for the projects_locations_glossaries resource."""

    _NAME = 'projects_locations_glossaries'

    def __init__(self, client):
      super(TranslateV3beta1.ProjectsLocationsGlossariesService, self).__init__(client)
      self._upload_configs = {
          }

    def Create(self, request, global_params=None):
      r"""Creates a glossary and returns the long-running operation. Returns NOT_FOUND, if the project doesn't exist.

      Args:
        request: (TranslateProjectsLocationsGlossariesCreateRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Create')
      return self._RunMethod(
          config, request, global_params=global_params)

    Create.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v3beta1/projects/{projectsId}/locations/{locationsId}/glossaries',
        http_method='POST',
        method_id='translate.projects.locations.glossaries.create',
        ordered_params=['parent'],
        path_params=['parent'],
        query_params=[],
        relative_path='v3beta1/{+parent}/glossaries',
        request_field='glossary',
        request_type_name='TranslateProjectsLocationsGlossariesCreateRequest',
        response_type_name='Operation',
        supports_download=False,
    )

    def Delete(self, request, global_params=None):
      r"""Deletes a glossary, or cancels glossary construction if the glossary isn't created yet. Returns NOT_FOUND, if the glossary doesn't exist.

      Args:
        request: (TranslateProjectsLocationsGlossariesDeleteRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Delete')
      return self._RunMethod(
          config, request, global_params=global_params)

    Delete.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v3beta1/projects/{projectsId}/locations/{locationsId}/glossaries/{glossariesId}',
        http_method='DELETE',
        method_id='translate.projects.locations.glossaries.delete',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v3beta1/{+name}',
        request_field='',
        request_type_name='TranslateProjectsLocationsGlossariesDeleteRequest',
        response_type_name='Operation',
        supports_download=False,
    )

    def Get(self, request, global_params=None):
      r"""Gets a glossary. Returns NOT_FOUND, if the glossary doesn't exist.

      Args:
        request: (TranslateProjectsLocationsGlossariesGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Glossary) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    Get.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v3beta1/projects/{projectsId}/locations/{locationsId}/glossaries/{glossariesId}',
        http_method='GET',
        method_id='translate.projects.locations.glossaries.get',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v3beta1/{+name}',
        request_field='',
        request_type_name='TranslateProjectsLocationsGlossariesGetRequest',
        response_type_name='Glossary',
        supports_download=False,
    )

    def List(self, request, global_params=None):
      r"""Lists glossaries in a project. Returns NOT_FOUND, if the project doesn't exist.

      Args:
        request: (TranslateProjectsLocationsGlossariesListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListGlossariesResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v3beta1/projects/{projectsId}/locations/{locationsId}/glossaries',
        http_method='GET',
        method_id='translate.projects.locations.glossaries.list',
        ordered_params=['parent'],
        path_params=['parent'],
        query_params=['filter', 'pageSize', 'pageToken'],
        relative_path='v3beta1/{+parent}/glossaries',
        request_field='',
        request_type_name='TranslateProjectsLocationsGlossariesListRequest',
        response_type_name='ListGlossariesResponse',
        supports_download=False,
    )

  class ProjectsLocationsOperationsService(base_api.BaseApiService):
    """Service class for the projects_locations_operations resource."""

    _NAME = 'projects_locations_operations'

    def __init__(self, client):
      super(TranslateV3beta1.ProjectsLocationsOperationsService, self).__init__(client)
      self._upload_configs = {
          }

    def Cancel(self, request, global_params=None):
      r"""Starts asynchronous cancellation on a long-running operation. The server makes a best effort to cancel the operation, but success is not guaranteed. If the server doesn't support this method, it returns `google.rpc.Code.UNIMPLEMENTED`. Clients can use Operations.GetOperation or other methods to check whether the cancellation succeeded or whether the operation completed despite cancellation. On successful cancellation, the operation is not deleted; instead, it becomes an operation with an Operation.error value with a google.rpc.Status.code of 1, corresponding to `Code.CANCELLED`.

      Args:
        request: (TranslateProjectsLocationsOperationsCancelRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Empty) The response message.
      """
      config = self.GetMethodConfig('Cancel')
      return self._RunMethod(
          config, request, global_params=global_params)

    Cancel.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v3beta1/projects/{projectsId}/locations/{locationsId}/operations/{operationsId}:cancel',
        http_method='POST',
        method_id='translate.projects.locations.operations.cancel',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v3beta1/{+name}:cancel',
        request_field='cancelOperationRequest',
        request_type_name='TranslateProjectsLocationsOperationsCancelRequest',
        response_type_name='Empty',
        supports_download=False,
    )

    def Delete(self, request, global_params=None):
      r"""Deletes a long-running operation. This method indicates that the client is no longer interested in the operation result. It does not cancel the operation. If the server doesn't support this method, it returns `google.rpc.Code.UNIMPLEMENTED`.

      Args:
        request: (TranslateProjectsLocationsOperationsDeleteRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Empty) The response message.
      """
      config = self.GetMethodConfig('Delete')
      return self._RunMethod(
          config, request, global_params=global_params)

    Delete.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v3beta1/projects/{projectsId}/locations/{locationsId}/operations/{operationsId}',
        http_method='DELETE',
        method_id='translate.projects.locations.operations.delete',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v3beta1/{+name}',
        request_field='',
        request_type_name='TranslateProjectsLocationsOperationsDeleteRequest',
        response_type_name='Empty',
        supports_download=False,
    )

    def Get(self, request, global_params=None):
      r"""Gets the latest state of a long-running operation. Clients can use this method to poll the operation result at intervals as recommended by the API service.

      Args:
        request: (TranslateProjectsLocationsOperationsGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    Get.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v3beta1/projects/{projectsId}/locations/{locationsId}/operations/{operationsId}',
        http_method='GET',
        method_id='translate.projects.locations.operations.get',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v3beta1/{+name}',
        request_field='',
        request_type_name='TranslateProjectsLocationsOperationsGetRequest',
        response_type_name='Operation',
        supports_download=False,
    )

    def List(self, request, global_params=None):
      r"""Lists operations that match the specified filter in the request. If the server doesn't support this method, it returns `UNIMPLEMENTED`. NOTE: the `name` binding allows API services to override the binding to use different resource name schemes, such as `users/*/operations`. To override the binding, API services can add a binding such as `"/v1/{name=users/*}/operations"` to their service configuration. For backwards compatibility, the default name includes the operations collection id, however overriding users must ensure the name binding is the parent resource, without the operations collection id.

      Args:
        request: (TranslateProjectsLocationsOperationsListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListOperationsResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v3beta1/projects/{projectsId}/locations/{locationsId}/operations',
        http_method='GET',
        method_id='translate.projects.locations.operations.list',
        ordered_params=['name'],
        path_params=['name'],
        query_params=['filter', 'pageSize', 'pageToken'],
        relative_path='v3beta1/{+name}/operations',
        request_field='',
        request_type_name='TranslateProjectsLocationsOperationsListRequest',
        response_type_name='ListOperationsResponse',
        supports_download=False,
    )

    def Wait(self, request, global_params=None):
      r"""Waits until the specified long-running operation is done or reaches at most a specified timeout, returning the latest state. If the operation is already done, the latest state is immediately returned. If the timeout specified is greater than the default HTTP/RPC timeout, the HTTP/RPC timeout is used. If the server does not support this method, it returns `google.rpc.Code.UNIMPLEMENTED`. Note that this method is on a best-effort basis. It may return the latest state before the specified timeout (including immediately), meaning even an immediate response is no guarantee that the operation is done.

      Args:
        request: (TranslateProjectsLocationsOperationsWaitRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Wait')
      return self._RunMethod(
          config, request, global_params=global_params)

    Wait.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v3beta1/projects/{projectsId}/locations/{locationsId}/operations/{operationsId}:wait',
        http_method='POST',
        method_id='translate.projects.locations.operations.wait',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v3beta1/{+name}:wait',
        request_field='waitOperationRequest',
        request_type_name='TranslateProjectsLocationsOperationsWaitRequest',
        response_type_name='Operation',
        supports_download=False,
    )

  class ProjectsLocationsService(base_api.BaseApiService):
    """Service class for the projects_locations resource."""

    _NAME = 'projects_locations'

    def __init__(self, client):
      super(TranslateV3beta1.ProjectsLocationsService, self).__init__(client)
      self._upload_configs = {
          }

    def BatchTranslateDocument(self, request, global_params=None):
      r"""Translates a large volume of document in asynchronous batch mode. This function provides real-time output as the inputs are being processed. If caller cancels a request, the partial results (for an input file, it's all or nothing) may still be available on the specified output location. This call returns immediately and you can use google.longrunning.Operation.name to poll the status of the call.

      Args:
        request: (TranslateProjectsLocationsBatchTranslateDocumentRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('BatchTranslateDocument')
      return self._RunMethod(
          config, request, global_params=global_params)

    BatchTranslateDocument.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v3beta1/projects/{projectsId}/locations/{locationsId}:batchTranslateDocument',
        http_method='POST',
        method_id='translate.projects.locations.batchTranslateDocument',
        ordered_params=['parent'],
        path_params=['parent'],
        query_params=[],
        relative_path='v3beta1/{+parent}:batchTranslateDocument',
        request_field='batchTranslateDocumentRequest',
        request_type_name='TranslateProjectsLocationsBatchTranslateDocumentRequest',
        response_type_name='Operation',
        supports_download=False,
    )

    def BatchTranslateText(self, request, global_params=None):
      r"""Translates a large volume of text in asynchronous batch mode. This function provides real-time output as the inputs are being processed. If caller cancels a request, the partial results (for an input file, it's all or nothing) may still be available on the specified output location. This call returns immediately and you can use google.longrunning.Operation.name to poll the status of the call.

      Args:
        request: (TranslateProjectsLocationsBatchTranslateTextRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('BatchTranslateText')
      return self._RunMethod(
          config, request, global_params=global_params)

    BatchTranslateText.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v3beta1/projects/{projectsId}/locations/{locationsId}:batchTranslateText',
        http_method='POST',
        method_id='translate.projects.locations.batchTranslateText',
        ordered_params=['parent'],
        path_params=['parent'],
        query_params=[],
        relative_path='v3beta1/{+parent}:batchTranslateText',
        request_field='batchTranslateTextRequest',
        request_type_name='TranslateProjectsLocationsBatchTranslateTextRequest',
        response_type_name='Operation',
        supports_download=False,
    )

    def DetectLanguage(self, request, global_params=None):
      r"""Detects the language of text within a request.

      Args:
        request: (TranslateProjectsLocationsDetectLanguageRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (DetectLanguageResponse) The response message.
      """
      config = self.GetMethodConfig('DetectLanguage')
      return self._RunMethod(
          config, request, global_params=global_params)

    DetectLanguage.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v3beta1/projects/{projectsId}/locations/{locationsId}:detectLanguage',
        http_method='POST',
        method_id='translate.projects.locations.detectLanguage',
        ordered_params=['parent'],
        path_params=['parent'],
        query_params=[],
        relative_path='v3beta1/{+parent}:detectLanguage',
        request_field='detectLanguageRequest',
        request_type_name='TranslateProjectsLocationsDetectLanguageRequest',
        response_type_name='DetectLanguageResponse',
        supports_download=False,
    )

    def Get(self, request, global_params=None):
      r"""Gets information about a location.

      Args:
        request: (TranslateProjectsLocationsGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Location) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    Get.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v3beta1/projects/{projectsId}/locations/{locationsId}',
        http_method='GET',
        method_id='translate.projects.locations.get',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v3beta1/{+name}',
        request_field='',
        request_type_name='TranslateProjectsLocationsGetRequest',
        response_type_name='Location',
        supports_download=False,
    )

    def GetSupportedLanguages(self, request, global_params=None):
      r"""Returns a list of supported languages for translation.

      Args:
        request: (TranslateProjectsLocationsGetSupportedLanguagesRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (SupportedLanguages) The response message.
      """
      config = self.GetMethodConfig('GetSupportedLanguages')
      return self._RunMethod(
          config, request, global_params=global_params)

    GetSupportedLanguages.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v3beta1/projects/{projectsId}/locations/{locationsId}/supportedLanguages',
        http_method='GET',
        method_id='translate.projects.locations.getSupportedLanguages',
        ordered_params=['parent'],
        path_params=['parent'],
        query_params=['displayLanguageCode', 'model'],
        relative_path='v3beta1/{+parent}/supportedLanguages',
        request_field='',
        request_type_name='TranslateProjectsLocationsGetSupportedLanguagesRequest',
        response_type_name='SupportedLanguages',
        supports_download=False,
    )

    def List(self, request, global_params=None):
      r"""Lists information about the supported locations for this service.

      Args:
        request: (TranslateProjectsLocationsListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListLocationsResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v3beta1/projects/{projectsId}/locations',
        http_method='GET',
        method_id='translate.projects.locations.list',
        ordered_params=['name'],
        path_params=['name'],
        query_params=['filter', 'pageSize', 'pageToken'],
        relative_path='v3beta1/{+name}/locations',
        request_field='',
        request_type_name='TranslateProjectsLocationsListRequest',
        response_type_name='ListLocationsResponse',
        supports_download=False,
    )

    def TranslateDocument(self, request, global_params=None):
      r"""Translates documents in synchronous mode.

      Args:
        request: (TranslateProjectsLocationsTranslateDocumentRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (TranslateDocumentResponse) The response message.
      """
      config = self.GetMethodConfig('TranslateDocument')
      return self._RunMethod(
          config, request, global_params=global_params)

    TranslateDocument.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v3beta1/projects/{projectsId}/locations/{locationsId}:translateDocument',
        http_method='POST',
        method_id='translate.projects.locations.translateDocument',
        ordered_params=['parent'],
        path_params=['parent'],
        query_params=[],
        relative_path='v3beta1/{+parent}:translateDocument',
        request_field='translateDocumentRequest',
        request_type_name='TranslateProjectsLocationsTranslateDocumentRequest',
        response_type_name='TranslateDocumentResponse',
        supports_download=False,
    )

    def TranslateText(self, request, global_params=None):
      r"""Translates input text and returns translated text.

      Args:
        request: (TranslateProjectsLocationsTranslateTextRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (TranslateTextResponse) The response message.
      """
      config = self.GetMethodConfig('TranslateText')
      return self._RunMethod(
          config, request, global_params=global_params)

    TranslateText.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v3beta1/projects/{projectsId}/locations/{locationsId}:translateText',
        http_method='POST',
        method_id='translate.projects.locations.translateText',
        ordered_params=['parent'],
        path_params=['parent'],
        query_params=[],
        relative_path='v3beta1/{+parent}:translateText',
        request_field='translateTextRequest',
        request_type_name='TranslateProjectsLocationsTranslateTextRequest',
        response_type_name='TranslateTextResponse',
        supports_download=False,
    )

  class ProjectsService(base_api.BaseApiService):
    """Service class for the projects resource."""

    _NAME = 'projects'

    def __init__(self, client):
      super(TranslateV3beta1.ProjectsService, self).__init__(client)
      self._upload_configs = {
          }

    def DetectLanguage(self, request, global_params=None):
      r"""Detects the language of text within a request.

      Args:
        request: (TranslateProjectsDetectLanguageRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (DetectLanguageResponse) The response message.
      """
      config = self.GetMethodConfig('DetectLanguage')
      return self._RunMethod(
          config, request, global_params=global_params)

    DetectLanguage.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v3beta1/projects/{projectsId}:detectLanguage',
        http_method='POST',
        method_id='translate.projects.detectLanguage',
        ordered_params=['parent'],
        path_params=['parent'],
        query_params=[],
        relative_path='v3beta1/{+parent}:detectLanguage',
        request_field='detectLanguageRequest',
        request_type_name='TranslateProjectsDetectLanguageRequest',
        response_type_name='DetectLanguageResponse',
        supports_download=False,
    )

    def GetSupportedLanguages(self, request, global_params=None):
      r"""Returns a list of supported languages for translation.

      Args:
        request: (TranslateProjectsGetSupportedLanguagesRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (SupportedLanguages) The response message.
      """
      config = self.GetMethodConfig('GetSupportedLanguages')
      return self._RunMethod(
          config, request, global_params=global_params)

    GetSupportedLanguages.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v3beta1/projects/{projectsId}/supportedLanguages',
        http_method='GET',
        method_id='translate.projects.getSupportedLanguages',
        ordered_params=['parent'],
        path_params=['parent'],
        query_params=['displayLanguageCode', 'model'],
        relative_path='v3beta1/{+parent}/supportedLanguages',
        request_field='',
        request_type_name='TranslateProjectsGetSupportedLanguagesRequest',
        response_type_name='SupportedLanguages',
        supports_download=False,
    )

    def TranslateText(self, request, global_params=None):
      r"""Translates input text and returns translated text.

      Args:
        request: (TranslateProjectsTranslateTextRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (TranslateTextResponse) The response message.
      """
      config = self.GetMethodConfig('TranslateText')
      return self._RunMethod(
          config, request, global_params=global_params)

    TranslateText.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v3beta1/projects/{projectsId}:translateText',
        http_method='POST',
        method_id='translate.projects.translateText',
        ordered_params=['parent'],
        path_params=['parent'],
        query_params=[],
        relative_path='v3beta1/{+parent}:translateText',
        request_field='translateTextRequest',
        request_type_name='TranslateProjectsTranslateTextRequest',
        response_type_name='TranslateTextResponse',
        supports_download=False,
    )
