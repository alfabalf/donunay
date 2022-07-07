import json
import uuid
import datetime
import re

import boto3

from django.test import TestCase
from django.conf import settings

from restapp.models import Album, Artifact


class ViewArtifactTests(TestCase):

    bucket = str(uuid.uuid4())
    session = boto3.session.Session(profile_name=settings.AWS_PROFILE)
    s3 = session.client("s3", region_name='ap-southeast-2', endpoint_url='http://localhost:4566')

    @staticmethod
    def artifact_data_payload(album_id):
        album_id = album_id
        caption = "the caption"
        details = "some describing details"
        date = datetime.date(1981, 6, 6)

        return {
            "album_id": album_id,
            "caption": caption,
            "details": details,
            "date": date
        }

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

    def test_create_artifact(self):

        album = Album.objects.create(name="test album", description="this is a description",
                                     cover_image_key='aaa/bbb', start_date=datetime.date(1981, 1, 1),
                                     end_date=datetime.date(1981, 12, 1))
        data = ViewArtifactTests.artifact_data_payload(album.id)

        with open('./restapp/tests/resources/sample_photo_front.jpg', 'rb') as image_front:
            with open('./restapp/tests/resources/sample_photo_back.jpg', 'rb') as image_back:
                form = {
                    "file0": image_front,
                    "file1": image_back,
                    "data": json.dumps(data, default=str)
                }
                response = self.client.post('/api/artifact/', data=form)

                uuid_regex = re.compile('^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z',
                                        re.I)

                assert response.status_code == 200
                assert response.data['caption'] == data['caption']
                assert response.data['details'] == data['details']
                assert response.data['date'] == data['date'].isoformat()

                pik = response.data['primary_image_key'].split('/')
                assert pik[0] == 'artifact'
                assert bool(uuid_regex.match(pik[1]))
                assert pik[2] == 'primary'

                pik = response.data['secondary_image_key'].split('/')
                assert pik[0] == 'artifact'
                assert bool(uuid_regex.match(pik[1]))
                assert pik[2] == 'secondary'

    def test_list_artifacts(self):
        album = ViewArtifactTests.create_album()
        artifact1 = Artifact.objects.create(album_id=album.id, caption="caption 1", details="details 1", date=datetime.date(1981, 9, 9),
                                primary_image_key="aaa/bbb", secondary_image_key="ccc/ddd")
        artifact2 = Artifact.objects.create(album_id=album.id, caption="caption 2", details="details 2",
                                date=datetime.date(1981, 10, 10),
                                primary_image_key="eee/fff", secondary_image_key="ggg/hhh")

        response = self.client.get('/api/artifact/', format='json')

        assert response.status_code == 200
        assert len(response.data) == 2
        assert response.data[0]['album'] == artifact1.album_id
        assert response.data[0]['caption'] == artifact1.caption
        assert response.data[0]['details'] == artifact1.details
        assert response.data[0]['date'] == artifact1.date.isoformat()
        assert response.data[0]['primary_image_key'] == artifact1.primary_image_key
        assert response.data[0]['secondary_image_key'] == artifact1.secondary_image_key

        assert response.data[1]['album'] == artifact2.album_id
        assert response.data[1]['caption'] == artifact2.caption
        assert response.data[1]['details'] == artifact2.details
        assert response.data[1]['date'] == artifact2.date.isoformat()
        assert response.data[1]['primary_image_key'] == artifact2.primary_image_key
        assert response.data[1]['secondary_image_key'] == artifact2.secondary_image_key

    def test_get_artifact(self):
        album = ViewArtifactTests.create_album()
        artifact = Artifact.objects.create(album_id=album.id, caption="caption 1", details="details 1", date=datetime.date(1981, 9, 9),
                                           primary_image_key="aaa/bbb", secondary_image_key="ccc/ddd")

        response = self.client.get('/api/artifact/{}'.format(artifact.id), format='json')

        assert response.status_code == 200
        assert response.data['album'] == artifact.album_id
        assert response.data['caption'] == artifact.caption
        assert response.data['details'] == artifact.details
        assert response.data['date'] == artifact.date.isoformat()
        assert response.data['primary_image_key'] == artifact.primary_image_key
        assert response.data['secondary_image_key'] == artifact.secondary_image_key

