import json
import uuid

from django.test import TestCase
from django.conf import settings

from restapp.models import Album

import boto3
import botocore


class APITests(TestCase):

    default_password = 'password'
    bucket = str(uuid.uuid4())
    session = boto3.session.Session(profile_name=settings.AWS_PROFILE)
    s3 = session.client("s3", region_name='ap-southeast-2', endpoint_url='http://localhost:4566')

    def setUp(self):
        try:
            self.s3.delete_bucket(Bucket=self.bucket)
        except Exception as e:
            pass
        self.s3.create_bucket(Bucket=self.bucket, CreateBucketConfiguration={'LocationConstraint': settings.AWS_REGION})

    def test_create_album(self):
        name = "album name"
        description = "a description" \
                      ""
        with open('./restapp/tests/resources/album_cover.jpeg', 'rb') as f:
            form = {
                "file": f,
                "json": json.dumps({"name": name, "description": description})
            }
            response = self.client.post('/api/album/', data=form)
            self.assertEqual(response.status_code, 200)

        album = Album.objects.all()[0]
        assert album.name == name
        assert album.description == description
        assert str(album.uuid) in album.cover_image_key

    def test_create_album_fails_when_cannot_write_to_bucket(self):
        name = "the album name"
        description = "a description"

        with open('./restapp/tests/resources/album_cover.jpeg', 'rb') as f:
            form = {
                "file": f,
                "json": json.dumps({"name": name, "description": description})
            }
            response = self.client.post('/api/album/', data=form)
            self.assertEqual(response.status_code, 200)

        album = Album.objects.all()[0]
        assert album.name == name
        assert album.description == description
        assert str(album.uuid) in album.cover_image_key


    def test_get_album(self):
        album = Album.objects.create(uuid=str(uuid.uuid4()), name="test album", description="this is a description", )
        response = self.client.get('/api/album/', format='json')

        assert response.status_code == 200
        assert response.data[0]['name'] == album.name
        assert response.data[0]['description'] == album.description

