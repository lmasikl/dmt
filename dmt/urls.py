from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django import forms
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, CreateView


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
        return super(RegisterView, self).form_valid(form)

    def get_success_url(self):
        return reverse('home')


urlpatterns = patterns('',
    url(
        r'^$',
        login_required(TemplateView.as_view(template_name='home.html')),
        name='home'
    ),
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
