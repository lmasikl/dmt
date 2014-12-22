# coding=utf-8
from media_bank.documents import Post
from tastypie.authentication import Authentication
from tastypie.authorization import DjangoAuthorization
from tastypie.exceptions import Unauthorized
from tastypie_mongoengine import resources

__project__ = 'dmt'


class Authorization(DjangoAuthorization):
    def read_list(self, object_list, bundle):
        klass = self.base_checks(bundle.request, object_list._document)

        if klass is False:
            return []

        # GET-style methods are always allowed.
        return object_list

    def create_detail(self, object_list, bundle):
        klass = self.base_checks(bundle.request, bundle.obj.__class__)

        if klass is False:
            raise Unauthorized("You are not allowed to access that resource.")

        return True


class PostResource(resources.MongoEngineResource):

    class Meta:
        resource_name = 'post'
        queryset = Post.objects.all()
        allowed_methods = ['get', 'post', 'put', 'delete']
        always_return_data = True
        authentication = Authentication()
        authorization = Authorization()