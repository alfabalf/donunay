import boto3


class Bucket(object):
    __monostate = None

    def __init__(self, aws_profile=None, s3_bucket=None, endpoint_url=None, aws_region=None):
        if Bucket.__monostate:
            self.__dict__ = Bucket.__monostate
        elif not Bucket.__monostate and aws_profile and s3_bucket and endpoint_url and aws_region:
            Bucket.__monostate = self.__dict__
            self.client = boto3.client("s3", region_name=aws_region, endpoint_url=endpoint_url)
            self.s3_bucket = s3_bucket
            self.aws_profile = aws_profile
            self.aws_region = aws_region
            self.endpoint_url = endpoint_url
        else:
            raise ValueError("Singleton must be instantiated first with parameters")


    def bucket_exists(self, bucket_name):
        try:
            self.client.get_bucket_acl(Bucket=bucket_name)
            return True
        except Exception as e:
            raise self.S3ClientException("{}".format(str(e)), self)

    def write_file(self, file_path, key):
        try:
             self.client.upload_file(
                file_path, self.s3_bucket, key)
        except Exception as e:
            raise self.S3ClientException("could not write file: {}".format(str(e)), self)

    def write_binary(self, bytes_io, key):
        try:
             self.client.put_object(
                Body=bytes_io, Bucket=self.s3_bucket, Key=key)
        except Exception as e:
            raise self.S3ClientException("could not write binary file: {}".format(str(e)), self)

    def _get_object(self, key):
        return self.client.get_object(Bucket=self.s3_bucket, Key=key)

    def object_exists(self, key):
        try:
             self._get_object(key)
             return True
        except Exception as e:
            raise self.S3ClientException("{}".format(str(e)), self)

    def get_object_content_text(self, key):

        try:
             return self._get_object(key)['Body'].read().decode('utf-8')
        except Exception as e:
            raise self.S3ClientException("could not get text: {}".format(str(e)), self)

    class S3ClientException(Exception):

        def __init__(self, message, obj):
            self.s3_bucket = obj.s3_bucket
            self.aws_profile = obj.aws_profile
            self.endpoint_url = obj.endpoint_url
            self.aws_region = obj.aws_region
            self.message = message

            super().__init__(self.message)

        def __str__(self):
            _str = "{message} (s3_bucket={s3_bucket}, aws_profile={aws_profile}, endpoint_url={endpoint_url}, " \
                       "aws_region={aws_region})"
            return _str.format(
                    message=self.message, s3_bucket=self.s3_bucket,
                    aws_profile=self.aws_profile, endpoint_url=self.endpoint_url, aws_region=self.aws_region)


if __name__ == '__main__':
    try:
        client1 = Bucket()
    except ValueError:
        pass

    client2 = Bucket(
        aws_profile='localstack', s3_bucket='test', endpoint_url='http://localhost:4566', aws_region='ap-southeast-2')
    client3 = Bucket()
    client4 = Bucket(
        aws_profile='localstack', s3_bucket='test', endpoint_url='http://localhost:4566', aws_region='ap-southeast-2')

    if client2.__dict__ is client3.__dict__:
        print("instances have same state")
