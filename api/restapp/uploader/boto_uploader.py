import boto3
from botocore.exceptions import ClientError


class S3Client:
    def __init__(self, aws_profile, s3_bucket, endpoint_url, aws_region):
        self.s3_bucket = s3_bucket
        boto3.setup_default_session(profile_name=aws_profile)
        self.client = boto3.client(
            "s3", region_name=aws_region, endpoint_url=endpoint_url)

    def put_object(self, file_path, key):

        try:
             self.client.upload_file(
                file_path, self.s3_bucket, key)
        except ClientError:
            print('could not put object')
            raise

    def _get_object(self, key):
        return self.client.get_object(Bucket=self.s3_bucket, Key=key)

    def object_exists(self, key):

        try:
             self._get_object(key)
             return True
        except ClientError:
            return False

    def get_object_content_text(self, key):

        try:
             return self._get_object(key)['Body'].read().decode('utf-8')
        except ClientError:
            return False
