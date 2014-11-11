from django.contrib.auth.models import User
from django.db import models
from djangotoolbox.fields import ListField, EmbeddedModelField


class File(models.Model):
    date = models.DateField(auto_now=True)
    size = models.PositiveIntegerField(default=0)
    type = models.CharField(max_length=4)
    comments = ListField(EmbeddedModelField('Comment'))


class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)
    text = models.TextField()
