import os
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from dotenv import load_dotenv


def upload_to_s3(file_path, object_name):
    load_dotenv()

    s3 = boto3.client(
        's3',
        endpoint_url=os.getenv('S3_ENDPOINT_URL'),
        region_name='ru-1',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        config=Config(s3={'addressing_style': 'path'})
    )

    bucket_name = os.getenv('S3_BUCKET_NAME')

    try:
        s3.upload_file(file_path, bucket_name, object_name)
        print('file loaded')
        image_url = f'{os.getenv('S3_ENDPOINT_URL')
                       }/{bucket_name}/{object_name}'
        return image_url
    except ClientError as e:
        print(f'Upload failed: {e}')
        return None
