# coding=utf-8
from django.contrib.auth.models import User

from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie.resources import ModelResource
from tastypie.api import Api
from tastypie.validation import Validation

from mediabank.models import File


class OwnerResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        resource_name = 'owner'
        # excludes = ['email', 'password', 'is_superuser']


class FileResource(ModelResource):
    owner = fields.ForeignKey(OwnerResource, 'owner')

    class Meta:
        queryset = File.objects.all()
        object_class = File
        resource_name = 'file'
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        allowed_methods = ['get', 'post', 'put', 'delete']
        always_return_data = True
        validation = Validation()
        filtering = {
            'owner': ALL_WITH_RELATIONS,
        }

    def dehydrate(self, bundle):
        return bundle

    def deserialize(self, request, data, format='application/json'):
        deserialized = super(FileResource, self).deserialize(request, data, format)
        deserialized.update({'owner': request.user})
        return deserialized

    def post_list(self, request, **kwargs):
        """
        Костыль
        """
        request.META['CONTENT_TYPE'] = 'application/json; charset=UTF-8'
        return super(FileResource, self).post_list(request, **kwargs)

    def put_detail(self, request, **kwargs):
        """
        Костыль
        """
        request.META['CONTENT_TYPE'] = 'application/json; charset=UTF-8'
        return super(FileResource, self).put_detail(request, **kwargs)


api = Api(api_name='v1')
api.register(FileResource())
api.register(OwnerResource())