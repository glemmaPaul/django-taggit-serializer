from rest_framework import serializers

from .models import TestModel
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)


class TestModelSerializer(TaggitSerializer, serializers.ModelSerializer):

    tags = TagListSerializerField()

    class Meta:
        model = TestModel
        fields = '__all__'