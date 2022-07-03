import re

from rest_framework import serializers

from .models import Album


def validate_s3_key(value):
    if not re.match("^[a-zA-Z0-9!_.*'()-]+(/[a-zA-Z0-9!_.*'()-]+)*$", value):
        raise serializers.ValidationError("not a valid s3 object key")


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'

    def validate_image_key(self, value):
        validate_s3_key(value)
        return value


class ArtifactSerializer(serializers.ModelSerializer):

    def validate_primary_image_key(self, value):
        validate_s3_key(value)
        return value

    def validate_secondary_image_key(self, value):
        validate_s3_key(value)
        return value