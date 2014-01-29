from django.conf.urls import patterns, include, url

from . import views 

urlpatterns = patterns('',
    url(
        regex=r'^$',
        view=views.PostListView.as_view(),
        name="home",
    ),
    url(
        regex=r'^new/$',
        view=views.PostCreateView.as_view(),
        name="new_post",
    ),
    url(
        regex=r'^(?P<slug>[\w-]+)/$',
        view=views.PostDetailView.as_view(),
        name="post",
    ),
    url(
        regex=r'^(?P<reply>[\w-]+)/reply/$',
        view=views.PostCreateView.as_view(),
        name="reply",
    ),
)
