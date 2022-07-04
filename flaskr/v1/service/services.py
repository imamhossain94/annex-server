import base64
from io import BytesIO
from PIL import Image
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from flaskr.v1.constants import *

# service account of the firebase project
cred = credentials.Certificate("serviceAccountKey.json")
# storage bucket of the firebase project
firebase_admin.initialize_app(cred, {'storageBucket': 'bubt-smart-routine.appspot.com'})


# decode base64 string and upload it into firebase to get short image link
def convertAndUploadImage(file_name, string_file):
    try:
        # first try to open the base64 image string
        im = Image.open(BytesIO(
            base64.b64decode(string_file.replace('data:image/png;base64,', '').replace('data:image/gif;base64,', ''))))

        # if the base64 string is valid then save the image into the images directory
        im.save(imageDirPath % file_name, 'PNG')

        # create a storage bucket object
        bucket = storage.bucket()

        # create a blob object for the image
        blob = bucket.blob(studentStorageBucketPath % file_name)

        # upload the images
        blob.upload_from_filename(imageDirPath % file_name)

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


def uploadImage(file_name):
    try:
        # create a storage bucket object
        bucket = storage.bucket()
        # create a blob object for the image
        blob = bucket.blob(routineStorageBucketPath % file_name)

        # upload the images
        blob.upload_from_filename(screenshotDirPath + file_name + '.png')

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
