from django.test import TestCase

from restapp.serializers import AlbumSerializer


class APITests(TestCase):

    def test_album_serializer_validates_cover_image_key(self):
        data = {"name": "some name", "description": "a description", "cover_image_key": "bad./key"}
        serializer = AlbumSerializer(data)

