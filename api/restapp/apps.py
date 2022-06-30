from django.apps import AppConfig
from django.conf import settings

import boto3


class RestappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'restapp'

    def ready(self):
        s3 = boto3.resource('s3', region_name=settings.AWS_REGION, endpoint_url=settings.ENDPOINT_URL)

        if s3.Bucket(settings.S3_BUCKET) not in s3.buckets.all():
            print("{bucket} bucket does not exist in {endpoint}"
                  .format(bucket=settings.S3_BUCKET, endpoint=settings.ENDPOINT_URL))
            s3.create_bucket(Bucket=settings.S3_BUCKET, CreateBucketConfiguration={'LocationConstraint': settings.AWS_REGION})
            print("{bucket} created in {endpoint}"
                  .format(bucket=settings.S3_BUCKET, endpoint=settings.ENDPOINT_URL))
        else:
            print("{bucket} already exists in {endpoint}"
                  .format(bucket=settings.S3_BUCKET, endpoint=settings.ENDPOINT_URL))

