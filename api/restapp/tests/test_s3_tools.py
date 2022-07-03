import uuid

from django.test import TestCase
from django.conf import settings
import boto3

from restapp.uploader.s3_tools import Bucket


class BucketTests(TestCase):

    bucket = settings.S3_BUCKET
    session = boto3.session.Session(profile_name=settings.AWS_PROFILE)
    s3 = session.client("s3", region_name='ap-southeast-2', endpoint_url='http://localhost:4566')

    def setUp(self):
        try:
            self.s3.create_bucket(Bucket=self.bucket, CreateBucketConfiguration={'LocationConstraint': settings.AWS_REGION})
        except:
            pass

    def configured_client(self):
        return Bucket(settings.AWS_PROFILE, self.bucket, settings.ENDPOINT_URL, settings.AWS_REGION)

    def test_s3_client_can_put_and_get_object(self):
        test_file = '/tmp/test.txt'
        key = 'xxx/yyy/zzz'
        content = 'abcd'

        with open(test_file, 'w') as f:
            f.write(content)

        client = self.configured_client()
        client.write_file(test_file, key)

        assert client.object_exists(key)
        assert client.get_object_content_text(key) == content

    def test_s3_client_can_delete_object(self):
        key = 'the/key'

        client = self.configured_client()
        client.write_binary(open('./restapp/tests/resources/sample_album_cover.jpg', 'rb'), key)
        assert self.s3.get_object(Bucket=self.bucket, Key=key)

        client = self.configured_client()
        client.delete_object(key)

        try:
            self.s3.get_object(Bucket=self.bucket, Key=key)
        except:
            assert True
