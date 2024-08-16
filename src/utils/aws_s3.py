import os
from boto3 import client as boto3Client
from botocore import exceptions as botocoreExceptions
from config.config import config

def upload_to_s3(file_name: str, bucket: str, object_name=None) -> None:
    s3_client = boto3Client(
        's3',
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
    )

    try:
        if object_name is None:
            object_name = file_name

        s3_client.upload_file(file_name, bucket, object_name)
    except botocoreExceptions.ClientError:
        print('Upload file ({file_name}) to s3 is not successfully')
