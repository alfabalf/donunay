import json
import uuid
import datetime

from django.test import TestCase
from django.conf import settings

from restapp.models import Album

import boto3


class ViewAlbumTests(TestCase):

    default_password = 'password'
    bucket = str(uuid.uuid4())
    session = boto3.session.Session(profile_name=settings.AWS_PROFILE)
    s3 = session.client("s3", region_name='ap-southeast-2', endpoint_url='http://localhost:4566')

    @staticmethod
    def album_data_payload_with_unique_name():
        description = "a description"
        start_date = datetime.date(1981, 1, 1)
        end_date = datetime.date(1981, 12, 1)

        return {
            "name": str(uuid.uuid4()),
            "description": description,
            "start_date": start_date,
            "end_date": end_date
        }

    def setUp(self):
        try:
            self.s3.delete_bucket(Bucket=self.bucket)
        except Exception as e:
            pass
        self.s3.create_bucket(Bucket=self.bucket, CreateBucketConfiguration={'LocationConstraint': settings.AWS_REGION})


    def test_create_album(self):
        data = ViewAlbumTests.album_data_payload_with_unique_name()

        with open('./restapp/tests/resources/sample_album_cover.jpg', 'rb') as f:
            form = {
                "file": f,
                "data": json.dumps(data, default=str)
            }
            response = self.client.post('/api/album/', data=form)
            self.assertEqual(response.status_code, 200)

        album = Album.objects.all()[0]
        assert album.name == data['name']
        assert album.description == data['description']
        assert album.start_date == data['start_date']
        assert album.end_date == data['end_date']

    def test_list_albums(self):
        album1 = Album.objects.create(
            name="test album1", description="this is a description",
            cover_image_key='aaa/bbb', start_date=datetime.date(1981, 1, 1), end_date=datetime.date(1981, 12, 1))
        album2 = Album.objects.create(
            name="test album2", description="this is a description",
            cover_image_key='bbb/ccc', start_date=datetime.date(1981, 1, 1), end_date=datetime.date(1981, 12, 1))
        response = self.client.get('/api/album/', format='json')

        assert response.status_code == 200
        print(response.data[0])
        assert response.data[0]['name'] == album1.name
        assert response.data[0]['description'] == album1.description
        assert response.data[0]['cover_image_key'] == album1.cover_image_key
        assert response.data[0]['start_date'] == album1.start_date.isoformat()
        assert response.data[0]['end_date'] == album1.end_date.isoformat()
        assert response.data[1]['name'] == album2.name
        assert response.data[1]['description'] == album2.description
        assert response.data[1]['cover_image_key'] == album2.cover_image_key
        assert response.data[1]['start_date'] == album2.start_date.isoformat()
        assert response.data[1]['end_date'] == album2.end_date.isoformat()


    def test_get_album(self):
        album = Album.objects.create(
            name="test album1", description="this is a description",
            cover_image_key='aaa/bbb', start_date=datetime.date(1981, 1, 1), end_date=datetime.date(1981, 12, 1))
        response = self.client.get('/api/album/{}'.format(album.id), format='json')

        assert response.status_code == 200
        assert response.data['name'] == album.name
        assert response.data['description'] == album.description

