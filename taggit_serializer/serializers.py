# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework.exceptions import ParseError


class TagListSerializerField(serializers.Field):

    def to_internal_value(self, data):
        if type(data) is not list:
            raise ParseError("expected a list of data")
        return data

    def to_representation(self, obj):
        if type(obj) is not list:
            return [tag.name for tag in obj.all()]
        return obj
