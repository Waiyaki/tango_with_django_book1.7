from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

from registration.backends.simple.views import RegistrationView


class MyRegistrationView(RegistrationView):
    def get_success_url(self, request, user):
        return '/rango/'


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tango_with_django.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^$', include('rango.urls', namespace="rango")),
    url(r'^rango/', include('rango.urls', namespace="rango")),
    url(r'^admin/', include(admin.site.urls)),

    # Override the default registration pattern in accounts
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name="registration_register"),
    url(r'^accounts/', include('registration.backends.simple.urls')),
)


if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
         'serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
