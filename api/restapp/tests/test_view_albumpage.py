import json
import uuid
import datetime
import re

import boto3

from django.test import TestCase
from django.conf import settings

from restapp.models import Album, Artifact

from restapp.models import AlbumPage


class ViewAlbumPageTests(TestCase):

    bucket = str(uuid.uuid4())
    session = boto3.session.Session(profile_name=settings.AWS_PROFILE)
    s3 = session.client("s3", region_name='ap-southeast-2', endpoint_url='http://localhost:4566')

    @staticmethod
    def create_album():
        return Album.objects.create(name="test album", description="this is a description",
                                     cover_image_key='aaa/bbb', start_date=datetime.date(1981, 1, 1),
                                     end_date=datetime.date(1981, 12, 1))

    def setUp(self):
        try:
            self.s3.delete_bucket(Bucket=self.bucket)
        except Exception as e:
            pass
        self.s3.create_bucket(Bucket=self.bucket, CreateBucketConfiguration={'LocationConstraint': settings.AWS_REGION})

    def test_create_album_page(self):

        album = Album.objects.create(name="test album", description="this is a description",
                                     cover_image_key='aaa/bbb', start_date=datetime.date(1981, 1, 1),
                                     end_date=datetime.date(1981, 12, 1))

        with open('./restapp/tests/resources/sample_album_cover.jpg', 'rb') as album_page:

            form = {
                "file0": album_page,
                "data": json.dumps({'album_id': album.id}, default=str)
            }
            response = self.client.post('/api/album_page/', data=form)

            uuid_regex = re.compile('^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z',
                                    re.I)

            assert response.status_code == 200
            assert response.data['album'] == album.id

            pik = response.data['page_image_key'].split('/')
            assert pik[0] == 'album_page'
            assert bool(uuid_regex.match(pik[1]))

    def test_list_album_page(self):
        album = ViewAlbumPageTests.create_album()
        album_page1 = AlbumPage.objects.create(album_id=album.id, page_image_key='aaa/bbb')
        album_page2 = AlbumPage.objects.create(album_id=album.id, page_image_key='ccc/ddd')

        response = self.client.get('/api/album_page/', format='json')

        assert response.status_code == 200
        assert len(response.data) == 2
        assert response.data[0]['album'] == album.id
        assert response.data[0]['page_image_key'] == album_page1.page_image_key
        assert response.data[1]['album'] == album.id
        assert response.data[1]['page_image_key'] == album_page2.page_image_key


    def test_get_artifact(self):
        album = ViewAlbumPageTests.create_album()
        album_page = AlbumPage.objects.create(album_id=album.id, page_image_key='aaa/bbb')

        response = self.client.get('/api/album_page/{}'.format(album_page.id), format='json')

        assert response.status_code == 200
        assert response.data['album'] == album.id
        assert response.data['page_image_key'] == album_page.page_image_key


