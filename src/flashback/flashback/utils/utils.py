"""Utility functions"""

from google.cloud import storage


def list_all_jpg_from_gcs(bucket: str):
    """Returns a list of all jpgs in a bucket"""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket)
    blobs = bucket.list_blobs()
    jpgs = set()
    for blob in blobs:
        if blob.name.split(".")[-1] == "jpg":
            jpgs.add(blob.name)
    return jpgs


def get_jpg_from_bucket(bucket: str, file: str):
    """Returns a jpg from a bucket"""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket)
    blob = bucket.blob(file)

    return blob.download_as_bytes()
