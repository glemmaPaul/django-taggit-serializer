from django.db import models
from taggit.managers import TaggableManager


class TestModel(models.Model):
    tags = TaggableManager()
