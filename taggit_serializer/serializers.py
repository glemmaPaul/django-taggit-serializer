# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
import json

class TagList(list):
    def __add__(self, rhs):
        return TagList(list.__add__(self, rhs))
    
    def __getitem__(self, item):
        result = list.__getitem__(self, item)
        try:
            return TagList(result)
        except TypeError:
            return result
    
    def __str__(self):
        return json.dumps(self)

class TagListSerializerField(serializers.Field):
    child = serializers.CharField()
    default_error_messages = {
        'not_a_list': _('Expected a list of items but got type "{input_type}".'),
        'invalid_json': _('Invalid json list. A tag list submitted in string form must be valid json.'),
    }
    
    def to_internal_value(self, value):
        if isinstance(value, basestring):
            if not value:
                value = "[]"
            try:
                value = json.loads(value)
            except ValueError:
                self.fail('invalid_json')
        
        if not isinstance(value, list):
            self.fail('not_a_list', input_type=type(value).__name__)

        return [self.child.run_validation(s) for s in value]

    def to_representation(self, value):
        if not isinstance(value, TagList):
            if not isinstance(value, list):
                value = [tag.name for tag in value.all()]
            value = TagList(value)

        return value

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
            [getattr(tag_object, key).add(tag) for tag in tag_values]

        return tag_object

    def _pop_tags(self, validated_data):
        to_be_tagged = {}
        
        for key in self.fields.keys():
            field = self.fields[key]
            if isinstance(field, TagListSerializerField):
                to_be_tagged[key] = validated_data.pop(key)
        return (to_be_tagged, validated_data)
