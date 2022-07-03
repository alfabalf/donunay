import uuid
import json
import os
import io

from PIL import Image

from django.conf import settings
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Album
from .serializers import AlbumSerializer
from .uploader.s3_tools import Bucket


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
                ext = str(request.FILES['file']).split('.')[1]
                bucket.write_binary(request.FILES['file'], '{prefix}/original.{ext}'.format(prefix=cover_image_key, ext=ext))

                for thumbnail_size in settings.THUMBNAIL_SIZES:
                    image = Image.open(request.FILES['file'])
                    image.thumbnail(thumbnail_size)
                    img_byte_arr = io.BytesIO()
                    image.save(img_byte_arr, format=image.format)
                    img_byte_arr = img_byte_arr.getvalue()
                    bucket.write_binary(img_byte_arr, '{prefix}/thumb_{size1}_{size2}.{ext}'.format(
                        prefix=cover_image_key, size1=thumbnail_size[0], size2=thumbnail_size[1], ext=ext))

            except bucket.S3ClientException as e:
                return Response("could not store image")

            serializer.save()
        else:
            # delete the files from s3
            return Response(serializer.errors)

        return Response(serializer.data)


class AlbumDetail(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        serializer = AlbumSerializer(Album.objects.get(pk=pk))
        return Response(serializer.data)

