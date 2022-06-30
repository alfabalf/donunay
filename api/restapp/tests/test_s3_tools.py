import uuid

from django.test import TestCase
from django.conf import settings
import boto3

from restapp.uploader.s3_tools import Bucket


class BucketTests(TestCase):

    bucket = str(uuid.uuid4())
    s3 = boto3.client("s3", region_name='ap-southeast-2', endpoint_url='http://localhost:4566')

    def setUp(self):
        try:
            self.s3.delete_bucket(Bucket=self.bucket)
        except Exception as e:
            pass
        self.s3.create_bucket(Bucket=self.bucket, CreateBucketConfiguration={'LocationConstraint': settings.AWS_REGION})

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

