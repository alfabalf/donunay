import uuid
import json
import io

from PIL import Image

from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions.exceptions import DolunayValidationError
from .models import Album, Artifact, AlbumPage
from .serializers import AlbumSerializer, ArtifactSerializer, AlbumPageSerializer
from .uploader.s3_tools import Bucket


def image_extension_is_valid(ext):
    return ext.lower() in [allowed_ext.lower() for allowed_ext in settings.VALID_IMAGE_EXTENSIONS]


def create_thumbnail(_file, size):
    image = Image.open(_file)
    image.thumbnail(size)
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format=image.format)
    return img_byte_arr.getvalue()

class AuthTestView(APIView):
    http_method_names = ['get']
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response('ok')


class AlbumView(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = [AllowAny]

    def get(self, request):
        serializer = AlbumSerializer(Album.objects.all().order_by('id'), many=True)
        return Response(serializer.data)

    def post(self, request):

        if not image_extension_is_valid(request.FILES['file0'].name.split('.')[1]):
            raise DolunayValidationError(
                "image extension must be one of: {}".format(','.join(settings.VALID_IMAGE_EXTENSIONS)))

        _uuid = str(uuid.uuid4())
        cover_image_key = 'album/{uuid}'.format(uuid=_uuid)

        data = json.loads(request.data['data'])
        serializer = AlbumSerializer(data={
            'name': data['name'],
            'description': data['description'],
            'cover_image_key': cover_image_key,
            'start_date': data['start_date'],
            'end_date': data['end_date']})

        if serializer.is_valid():

            try:
                bucket = Bucket()
                ext = str(request.FILES['file0']).split('.')[1]
                bucket.write_binary(request.FILES['file0'], '{prefix}/original.{ext}'.format(prefix=cover_image_key, ext=ext))

                for thumbnail_size in settings.THUMBNAIL_SIZES:
                    img_byte_arr = create_thumbnail(request.FILES['file0'], thumbnail_size)
                    bucket.write_binary(img_byte_arr, '{prefix}/thumb_{size1}_{size2}.{ext}'.format(
                        prefix=cover_image_key, size1=thumbnail_size[0], size2=thumbnail_size[1], ext=ext))
            except bucket.S3ClientException as e:
                return APIException("could not store image")
            except Exception as e:
                raise APIException("could not create thumbnails: {}".format(e))

            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)


class AlbumDetail(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        serializer = AlbumSerializer(Album.objects.get(pk=pk))
        return Response(serializer.data)


class ArtifactView(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = [AllowAny]

    def get(self, request):
        serializer = ArtifactSerializer(Artifact.objects.all().order_by('id'), many=True)
        return Response(serializer.data)

    def post(self, request):

        if not image_extension_is_valid(request.FILES['file0'].name.split('.')[1]) \
                or not image_extension_is_valid(request.FILES['file1'].name.split('.')[1]):
            raise DolunayValidationError(
                "image extension must be one of: {}".format(','.join(settings.VALID_IMAGE_EXTENSIONS)))

        _uuid = str(uuid.uuid4())
        artifact_uuid_key = 'artifact/{uuid}'.format(uuid=_uuid)
        primary_image_key = '{}/primary'.format(artifact_uuid_key)
        secondary_image_key = '{}/secondary'.format(artifact_uuid_key)

        image_key_map = {'file0': primary_image_key, 'file1': secondary_image_key}

        data = json.loads(request.data['data'])
        serializer = ArtifactSerializer(data={
            'album': data['album_id'],
            'caption': data['caption'],
            'details': data['details'],
            'date': data['date'],
            'primary_image_key': primary_image_key,
            'secondary_image_key': secondary_image_key})

        bucket = Bucket()

        if serializer.is_valid():

            try:
                for upload_file in ['file0', 'file1']:
                    ext = str(request.FILES[upload_file]).split('.')[1]
                    bucket.write_binary(request.FILES[upload_file],
                                        '{prefix}/original.{ext}'.format(prefix=image_key_map[upload_file], ext=ext))

                    for thumbnail_size in settings.THUMBNAIL_SIZES:
                        img_byte_arr = create_thumbnail(request.FILES[upload_file], thumbnail_size)
                        bucket.write_binary(img_byte_arr, '{prefix}/thumb_{size1}_{size2}.{ext}'.format(
                            prefix=image_key_map[upload_file], size1=thumbnail_size[0], size2=thumbnail_size[1], ext=ext))

            except Bucket.S3ClientException as e:
                return APIException("could not store image")
            except Exception as e:
                raise APIException("could not create thumbnails: {}".format(e))
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)


class ArtifactDetail(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        serializer = ArtifactSerializer(Artifact.objects.get(pk=pk))
        return Response(serializer.data)


class AlbumPageView(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = [AllowAny]

    def get(self, request):
        serializer = AlbumPageSerializer(AlbumPage.objects.all().order_by('id'), many=True)
        return Response(serializer.data)

    def post(self, request):

        if not image_extension_is_valid(request.FILES['file0'].name.split('.')[1]):
            raise DolunayValidationError(
                "image extension must be one of: {}".format(','.join(settings.VALID_IMAGE_EXTENSIONS)))

        _uuid = str(uuid.uuid4())
        page_uuid_key = 'album_page/{uuid}'.format(uuid=_uuid)

        data = json.loads(request.data['data'])
        serializer = AlbumPageSerializer(data={
            'album': data['album_id'],
            'page_image_key': page_uuid_key})

        bucket = Bucket()

        if serializer.is_valid():

            try:
                bucket = Bucket()
                ext = str(request.FILES['file0']).split('.')[1]
                bucket.write_binary(request.FILES['file0'],
                                    '{prefix}/original.{ext}'.format(prefix=page_uuid_key, ext=ext))

                for thumbnail_size in settings.THUMBNAIL_SIZES:
                    img_byte_arr = create_thumbnail(request.FILES['file0'], thumbnail_size)
                    bucket.write_binary(img_byte_arr, '{prefix}/thumb_{size1}_{size2}.{ext}'.format(
                        prefix=page_uuid_key, size1=thumbnail_size[0], size2=thumbnail_size[1], ext=ext))
            except bucket.S3ClientException as e:
                return APIException("could not store image")
            except Exception as e:
                raise APIException("could not create thumbnails: {}".format(e))
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)

class AlbumPageDetail(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        serializer = AlbumPageSerializer(AlbumPage.objects.get(pk=pk))
        return Response(serializer.data)
