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
        regex=r'^(?P<slug>[\w-]+)/edit/$',
        view=views.PostUpdateView.as_view(),
        name="edit",
    ),
    url(
        regex=r'^(?P<reply>[\w-]+)/reply/$',
        view=views.PostCreateView.as_view(),
        name="reply",
    ),
    url(
        regex=r'^(?P<slug>[\w-]+)/root/$',
        view=views.RootView.as_view(),
        name="root",
    ),
    url(
        regex=r'^tags/$',
        view=views.TagsListView.as_view(),
        name="tags",
    ),
    url(
        regex=r'^tags/(?P<tag>[\w-]+)/$',
        view=views.PostTaggedView.as_view(),
        name="tagged_posts",
    ),
    url(
        regex=r'^by/(?P<author>[\w-]+)/$',
        view=views.AuthoredView.as_view(),
        name="author",
    ),
    url(
        regex=r'^(?P<slug>[\w-]+)/$',
        view=views.PostDetailView.as_view(),
        name="post",
    ),
)
