from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^',    include('dressings.urls')),
    url(
        regex=r'^accounts/login/$',
        view='django.contrib.auth.views.login',
        name="login"
    ),
    url(
        regex=r'^accounts/logout/$',
        view='django.contrib.auth.views.logout_then_login',
        name="logout"
    ),
    url(r'^admin/', include(admin.site.urls)),
)
