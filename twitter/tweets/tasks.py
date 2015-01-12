import httplib2
import os
import random
import sys
import time
import io

from apiclient.discovery import build as discovery_build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from apiclient.http import MediaIoBaseDownload
from apiclient.http import MediaIoBaseUpload
from json import dumps as json_dumps
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage as CredentialStorage
from oauth2client.tools import run as run_oauth2

from tweets import models

DIR = os.path.dirname(__file__)
CLIENT_SECRETS_FILE = os.path.join(DIR, 'security/client_secrets.json')
CREDENTIALS_FILE = os.path.join(DIR, 'security/credentials.json')
MISSING_CLIENT_SECRETS_MESSAGE = "Missing client secrets!!!"

RW_SCOPE = 'https://www.googleapis.com/auth/devstorage.read_write'
RO_SCOPE = 'https://www.googleapis.com/auth/devstorage.read_only'

# Mimetype to use if one can't be guessed from the file extension.
DEFAULT_MIMETYPE = 'application/octet-stream'


def get_authenticated_service(scope):
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=scope,
                                   message=MISSING_CLIENT_SECRETS_MESSAGE)

    credential_storage = CredentialStorage(CREDENTIALS_FILE)
    credentials = credential_storage.get()
    if credentials is None or credentials.invalid:
        credentials = run_oauth2(flow, credential_storage)

    http = credentials.authorize(httplib2.Http())
    return discovery_build('storage', 'v1', http=http)


def upload_file_to_google_cloud(fil, twitteruser_pk):
    bucket_name = 'jnp3-bucket'
    object_name = '__avatar__{}'.format(twitteruser_pk)

    service = get_authenticated_service(RW_SCOPE)

    media = MediaIoBaseUpload(fil.file, mimetype='image/png')
    request = service.objects().insert(bucket=bucket_name, name=object_name,
                                       media_body=media)
    res = request.execute()
    twitter_user = models.TwitterUser.objects.get(pk=twitteruser_pk)
    twitter_user.avatar_url = res['mediaLink']
    twitter_user.save()
