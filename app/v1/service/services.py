import base64
from io import BytesIO
from PIL import Image
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from app.v1.constants import *


firebase_credentials = {
    "type": os.environ.get("TYPE"),
    "project_id": os.environ.get("PROJECT_ID"),
    "private_key_id": os.environ.get("PRIVATE_KEY_ID"),
    "private_key": os.environ.get("PRIVATE_KEY").replace(r'\n', '\n'),
    "client_email": os.environ.get("CLIENT_EMAIL"),
    "client_id": os.environ.get("CLIENT_ID"),
    "auth_uri": os.environ.get("AUTH_URI"),
    "token_uri": os.environ.get("TOKEN_URI"),
    "auth_provider_x509_cert_url": os.environ.get("AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.environ.get("CLIENT_X509_CERT_URL")
}

# Auth google admin sdk
cred = credentials.Certificate(firebase_credentials)

# storage bucket of the firebase project
firebase_admin.initialize_app(cred, {'storageBucket': 'bubt-smart-routine.appspot.com'})


# decode base64 string and upload it into firebase to get short image link
def convertAndUploadImage(file_name, string_file):
    try:
        # first try to open the base64 image string
        im = Image.open(BytesIO(
            base64.b64decode(string_file.replace('data:image/png;base64,', '').replace('data:image/gif;base64,', ''))))

        # if the base64 string is valid then save the image as BytesIO
        buffer = BytesIO()
        im.save(buffer, format="JPEG", optimize=True)

        # create a storage bucket object
        bucket = storage.bucket()

        # create a blob object for the image
        blob = bucket.blob(studentStorageBucketPath % file_name)

        # upload the images
        blob.upload_from_string(buffer.getvalue(), content_type='image/jpeg')

        # Update blob's ACL, granting read access to anonymous users.
        blob.make_public()

        # return the images url
        return blob.public_url
    except Exception as e:
        print("Error Uploading Image :" + str(e))
        # if it failed to decode the base64 image
        # then it maybe an image path
        # so return the image path
        return dashboardUrl + string_file


def uploadImage(file_name, string_file):
    try:
        # first try to open the base64 image string
        im = Image.open(BytesIO(
            base64.b64decode(string_file.replace('data:image/png;base64,', '').replace('data:image/gif;base64,', ''))))
        rgb_im = im.convert('RGB')
        # if the base64 string is valid then save the image as BytesIO
        buffer = BytesIO()
        rgb_im.save(buffer, format="JPEG", optimize=True)

        # create a storage bucket object
        bucket = storage.bucket()
        # create a blob object for the image
        blob = bucket.blob(routineStorageBucketPath % file_name)

        # upload the images
        blob.upload_from_string(buffer.getvalue(), content_type='image/jpeg')

        # Update blob's ACL, granting read access to anonymous users.
        blob.make_public()

        # return the images url
        return blob.public_url
    except Exception as e:
        print("Error Uploading Image :" + str(e))
        # if it failed to decode the base64 image
        # then it maybe an image path
        # so return the image path
        return ''
