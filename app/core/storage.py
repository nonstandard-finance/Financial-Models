# core/storage.py
import boto3

from app.core.constants import BUCKET_NAME, AWS_ACCESS_KEY, AWS_SECRET_KEY, REGION

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=REGION,
)
