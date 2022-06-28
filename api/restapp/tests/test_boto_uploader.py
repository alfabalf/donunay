
from django.test import TestCase
from django.conf import settings

from restapp.uploader.boto_uploader import S3Client


class BotoUploaderTests(TestCase):

    def test_s3_client_can_put_and_get_object(self):
        test_file = '/tmp/test.txt'
        key = 'xxx/yyy/zzz'
        content = 'abcd'

        with open(test_file, 'w') as f:
            f.write(content)

        client = S3Client(settings.AWS_PROFILE, settings.S3_BUCKET, settings.ENDPOINT_URL, settings.AWS_REGION)
        client.put_object(test_file, key)

        assert client.object_exists(key)
        assert client.get_object_content_text(key) == content

