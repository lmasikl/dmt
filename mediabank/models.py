from django.contrib.auth.models import User
from django.db import models
from djangotoolbox.fields import ListField, EmbeddedModelField
from tastypie.models import create_api_key


class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)
    text = models.TextField()


class File(models.Model):
    date = models.DateField(auto_now=True)
    size = models.PositiveIntegerField(default=0)
    type = models.CharField(max_length=4)
    owner = models.ForeignKey(User)
    # owner = EmbeddedModelField(User)
    comments = models.ManyToManyField(Comment, blank=True, null=True)
    # comments = ListField(EmbeddedModelField('Comment'))


models.signals.post_save.connect(create_api_key, sender=User)
