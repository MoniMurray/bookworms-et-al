from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


# create custom class for static files
class StaticStorage(S3Boto3Storage):
    """
    Custom class to upload and store product images
    """

    location = settings.STATICFILES_LOCATION


# create custom class for MEDIA files
class MediaStorage(S3Boto3Storage):

    location = settings.MEDIAFILES_LOCATION
