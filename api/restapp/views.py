import uuid
import json

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
        serializer = AlbumSerializer(Album.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request):
        _uuid = str(uuid.uuid4())
        cover_image_key = 'album/{uuid}'.format(uuid=_uuid)

        try:
            client = Bucket(settings.AWS_PROFILE, settings.S3_BUCKET, settings.ENDPOINT_URL, settings.AWS_REGION)
            client.write_binary(request.FILES['file'], cover_image_key)
        except client.S3ClientException as e:
            return Response("could not store image")

        data = json.loads(request.data['data'])
        serializer = AlbumSerializer(data={'uuid': _uuid, 'name': data['name'], 'description': data['description'], 'cover_image_key': cover_image_key})

        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors)

        return Response(serializer.data)


class AlbumDetail(APIView):
    permission_classes = [AllowAny]

    def get(self, request, _uuid):
        serializer = AlbumSerializer(Album.objects.get(uuid=_uuid))
        return Response(serializer.data)

