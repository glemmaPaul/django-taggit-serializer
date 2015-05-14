# -*- coding: utf-8 -*-
from rest_framework import serializers


class TagListSerializerField(serializers.ListField):
    child = serializers.CharField()

    def to_representation(self, obj):
        if type(obj) is not list:
            return [tag.name for tag in obj.all()]
        return obj


class TaggitSerializer(serializers.Serializer):
    def create(self, validated_data):
        to_be_tagged, validated_data = self._pop_tags(validated_data)

        tag_object = super(TaggitSerializer, self).create(validated_data)

        return self._save_tags(tag_object, to_be_tagged)

    def update(self, object, validated_data):
        to_be_tagged, validated_data = self._pop_tags(validated_data)

        tag_object = super(TaggitSerializer, self).update(
            object, validated_data)

        return self._save_tags(tag_object, to_be_tagged)

    def _save_tags(self, tag_object, tags):
        for key in tags.keys():
            tag_values = tags.get(key)
            for tag in tag_values:
                getattr(tag_object, key).add(tag)

            for tag in tag_object.tags.names():
                if tag not in tag_values:
                    getattr(tag_object, key).remove(tag)

        return tag_object

    def _pop_tags(self, validated_data):
        to_be_tagged = {}

        for key in self.fields.keys():
            field = self.fields[key]
            if isinstance(field, TagListSerializerField):
                to_be_tagged[key] = validated_data.pop(key)

        return (to_be_tagged, validated_data)
