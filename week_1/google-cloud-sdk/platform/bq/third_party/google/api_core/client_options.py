#!/usr/bin/env python
"""Client options class.

Client options provide a consistent interface for user options to be defined
across clients.

You can pass a client options object to a client.

.. code-block:: python

    from google.api_core.client_options import ClientOptions
    from google.cloud.vision_v1 import ImageAnnotatorClient

    def get_client_cert():
        # code to load client certificate and private key.
        return client_cert_bytes, client_private_key_bytes

    options = ClientOptions(api_endpoint="foo.googleapis.com",
        client_cert_source=get_client_cert)

    client = ImageAnnotatorClient(client_options=options)

You can also pass a mapping object.

.. code-block:: python

    from google.cloud.vision_v1 import ImageAnnotatorClient

    client = ImageAnnotatorClient(
        client_options={
            "api_endpoint": "foo.googleapis.com",
            "client_cert_source" : get_client_cert
        })


"""


class ClientOptions(object):
    """Client Options used to set options on clients.

    Args:
        api_endpoint (Optional[str]): The desired API endpoint, e.g.,
            compute.googleapis.com
        client_cert_source (Optional[Callable[[], (bytes, bytes)]]): A callback
            which returns client certificate bytes and private key bytes both in
            PEM format. ``client_cert_source`` and ``client_encrypted_cert_source``
            are mutually exclusive.
        client_encrypted_cert_source (Optional[Callable[[], (str, str, bytes)]]):
            A callback which returns client certificate file path, encrypted
            private key file path, and the passphrase bytes.``client_cert_source``
            and ``client_encrypted_cert_source`` are mutually exclusive.
        quota_project_id (Optional[str]): A project name that a client's
            quota belongs to.
        credentials_file (Optional[str]): A path to a file storing credentials.
            ``credentials_file` and ``api_key`` are mutually exclusive.
        scopes (Optional[Sequence[str]]): OAuth access token override scopes.
        api_key (Optional[str]): Google API key. ``credentials_file`` and
            ``api_key`` are mutually exclusive.

    Raises:
        ValueError: If both ``client_cert_source`` and ``client_encrypted_cert_source``
            are provided, or both ``credentials_file`` and ``api_key`` are provided.
    """

    def __init__(
        self,
        api_endpoint=None,
        client_cert_source=None,
        client_encrypted_cert_source=None,
        quota_project_id=None,
        credentials_file=None,
        scopes=None,
        api_key=None,
    ):
        if client_cert_source and client_encrypted_cert_source:
            raise ValueError(
                "client_cert_source and client_encrypted_cert_source are mutually exclusive"
            )
        if api_key and credentials_file:
            raise ValueError("api_key and credentials_file are mutually exclusive")
        self.api_endpoint = api_endpoint
        self.client_cert_source = client_cert_source
        self.client_encrypted_cert_source = client_encrypted_cert_source
        self.quota_project_id = quota_project_id
        self.credentials_file = credentials_file
        self.scopes = scopes
        self.api_key = api_key

    def __repr__(self):
        return "ClientOptions: " + repr(self.__dict__)


def from_dict(options):
    """Construct a client options object from a mapping object.

    Args:
        options (collections.abc.Mapping): A mapping object with client options.
            See the docstring for ClientOptions for details on valid arguments.
    """

    client_options = ClientOptions()

    for key, value in options.items():
        if hasattr(client_options, key):
            setattr(client_options, key, value)
        else:
            raise ValueError("ClientOptions does not accept an option '" + key + "'")

    return client_options
