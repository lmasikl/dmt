# coding=utf-8
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource
from tastypie.api import Api

from mediabank.models import File


class FileResource(ModelResource):

    class Meta:
        queryset = File.objects.all()
        resource_name = 'file'
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get', 'post', 'put', 'delete']


api = Api(api_name='v1')
api.register(FileResource())