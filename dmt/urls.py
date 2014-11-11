from django.conf.urls import patterns, include, url
from django.contrib.auth.models import User
from django import forms
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from mediabank.api import api


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.set_password(self.object.password)
        self.object.save()
        return HttpResponseRedirect(reverse('bank:list'))


urlpatterns = patterns('',
    url(r'^$', include('mediabank.urls', namespace='bank')),
    url(r'^api/', include(api.urls)),
    url(
        r'^register/$',
        RegisterView.as_view(),
        kwargs={'template_name': 'register.html'},
        name='register'
    ),
    url(
        r'^login/$',
        'django.contrib.auth.views.login',
        kwargs={'template_name': 'login.html'},
        name='login'
    ),
    url(
        r'^logout/$',
        'django.contrib.auth.views.logout_then_login',
        name='logout'
    ),
)
