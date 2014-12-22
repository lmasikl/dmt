from django.conf.urls import patterns, include, url
from tastypie.api import Api
from media_bank.api import PostResource

api = Api(api_name='v1')
api.register(PostResource())

urlpatterns = patterns(
    '',
    url(r'^api/', include(api.urls)),
)
