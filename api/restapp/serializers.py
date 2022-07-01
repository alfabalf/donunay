import re

from rest_framework import serializers

from .models import Album


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'

    def validate_cover_image_key(self, value):
        if not re.match("^[a-zA-Z0-9!_.*'()-]+(/[a-zA-Z0-9!_.*'()-]+)*$", value):
            raise serializers.ValidationError("not a valid s3 object key")
        return value
