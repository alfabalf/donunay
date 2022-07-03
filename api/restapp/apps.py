from django.apps import AppConfig
from django.conf import settings

import boto3

from restapp.uploader.s3_tools import Bucket


class RestappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'restapp'

    def ready(self):
        session = boto3.session.Session(profile_name=settings.AWS_PROFILE)
        client = session.client("s3", region_name=settings.AWS_REGION, endpoint_url=settings.ENDPOINT_URL)
        try:
            client.create_bucket(Bucket=settings.S3_BUCKET, CreateBucketConfiguration={'LocationConstraint': settings.AWS_REGION})
            print("created bucket {}".format(settings.S3_BUCKET))
        except Exception as e:
            print(e)

        # initialise Singleton Bucket tool
        Bucket(settings.AWS_PROFILE, settings.S3_BUCKET, settings.ENDPOINT_URL, settings.AWS_REGION)



