from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

from post.views import CustomRegistrationView
from post.forms import LoginForm

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),


    url(r'^', include('post.urls')),

    url(
        regex=r'^accounts/register/$',
        view=CustomRegistrationView.as_view(),
        name="register",
    ),
    url(
        regex=r'^accounts/login/$',
        view='django.contrib.auth.views.login',
        name="login",
        kwargs={
            'authentication_form': LoginForm,
            'template_name': 'registration/login.html'
        },
    ),
    url(
        regex=r'^accounts/logout/$',
        view='django.contrib.auth.views.logout_then_login',
        name="logout",
    ),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (
            r'^static/(?P<path>.*)$',
             'django.views.static.serve',
            {
                'document_root': settings.STATIC_ROOT
            }
        ),
        (
            r'^media/(?P<path>.*)$',
             'django.views.static.serve',
            {
                'document_root': settings.MEDIA_ROOT
            }
        ),
    )
