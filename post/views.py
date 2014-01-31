from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse_lazy, reverse

from vanilla import ListView, DetailView, CreateView, UpdateView, RedirectView
from braces.views import LoginRequiredMixin
from core import views as core_views
from taggit.models import Tag
from registration.backends.simple.views import RegistrationView

from . import models
from . import forms


class PostListView(core_views.TermSearchMixin, ListView):
    model = models.Post
    term_mapping = {
        "title": "icontains",
        "tags__name": "iexact",
    }

    def get_queryset(self):
        queryset = super(PostListView, self).get_queryset()
        return queryset.originals().are_active()


class PostDetailView(core_views.TagsContextMixin, DetailView):
    model = models.Post
    lookup_field = "slug"

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['replies'] = self.object.replies.select_related()
        context['include_template'] = "post/includes/post_include.html"
        return context


class PostCreateView(LoginRequiredMixin, core_views.AuthoredMixin, CreateView):

    model = models.Post

    def get_success_url(self):
        if self.kwargs.get('reply', None):
            return self.get_previous().get_absolute_url()
        return self.object.get_absolute_url()

    def get_form_class(self):
        if self.kwargs.get('reply', None):
            return forms.ReplyForm
        return forms.PostForm

    def get_previous(self):
        if not hasattr(self, "previous"):
            self.previous = get_object_or_404(self.model, slug=self.kwargs['reply'])
        return self.previous

    def get_context_data(self, **kwargs):
        context = super(PostCreateView, self).get_context_data(**kwargs)
        if self.kwargs.get('reply', None):
            context['previous'] = self.get_previous()
        else:
            context['title'] = "New Post"
        return context

    def form_valid(self, form):
        if form.is_valid():
            if self.kwargs.get('reply', None):
                form.instance.title = "re: {}{}".format(
                    self.get_previous().title,
                    " ({})".format(
                        self.get_previous().replies.count()
                    ) if self.get_previous().replies.count() else ""
                )
                form.instance.previous = self.get_previous()
                form.save()
        return super(PostCreateView, self).form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Post
    lookup_field = "slug"
    form_class = forms.PostForm

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super(PostUpdateView, self).get_context_data(**kwargs)
        context['title'] = "Edit Post"
        return context


class PostTaggedView(PostListView):

    def get_queryset(self):
        queryset = super(PostTaggedView, self).get_queryset()
        return queryset.filter(
            tags__name=self.kwargs['tag']
        ).distinct()


class AuthoredView(PostListView):

    def get_queryset(self):
        queryset = super(AuthoredView, self).get_queryset()
        return queryset.filter(
            author__username=self.kwargs['author']
        )


class RootView(RedirectView):

    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(models.Post, slug=self.kwargs['slug'])
        while post.previous is not None:
            post = post.previous
        return post.get_absolute_url()


class TagsListView(ListView):

    model = Tag


class CustomRegistrationView(RegistrationView):

    form_class = forms.RegisterForm

    def get_success_url(self, request, user):
        return reverse("home")
