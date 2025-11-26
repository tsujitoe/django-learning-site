"""
Custom storage backends for the project.
"""
from django.conf import settings
from storages.backends.gcloud import GoogleCloudStorage


class MediaStorage(GoogleCloudStorage):
    """Google Cloud Storage for media files."""
    bucket_name = settings.GCS_BUCKET_NAME
    file_overwrite = False
    default_acl = 'publicRead'
