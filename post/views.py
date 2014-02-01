from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse_lazy, reverse
from django.conf import settings 

from vanilla import ListView, DetailView, CreateView, UpdateView, RedirectView, TemplateView
from braces.views import LoginRequiredMixin
from core import views as core_views
from taggit.models import Tag
from registration.backends.simple.views import RegistrationView

from . import models
from . import forms


class PostListView(
    core_views.ContextVariableMixin,
    core_views.TermSearchMixin,
    ListView
):
    model = models.Post
    term_mapping = {
        "title": "icontains",
        "tags__name": "iexact",
    }
    context_head = "All Posts"
    context_lead = "Some posts will be found below. Eventually."

    def get_queryset(self):
        return super(
            PostListView, self
        ).get_queryset().originals()


class PostDetailView(core_views.TagsContextMixin, DetailView):
    model = models.Post
    lookup_field = "slug"

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['replies'] = self.object.replies.select_related()
        context['include_template'] = "post/includes/post_include.html"
        return context

    def get_object(self):
        queryset = self.get_queryset()
        slug = self.kwargs[self.lookup_field]
        if self.request.user.is_authenticated():
            if self.request.user.is_staff:
                return get_object_or_404(
                    queryset,
                    slug=slug
                )
        return get_object_or_404(
            queryset,
            slug=slug,
            active=True
        )


class PostCreateView(LoginRequiredMixin, core_views.AuthoredMixin, CreateView):

    model = models.Post

    def create_reply(self):
        models.Email.objects.create(
            subject="Your post received a reply!",
            content="""
            Dear {user}, 

            Your post on Post-Thing received a reply from {other_user}! 

            Please click <a href="{site_url}/{url}">here</a> to view the response.

            Regards,
            The Team at Post-Thing. 
            """.format(
                user=self.get_previous().author.username,
                other_user=self.request.user.username,
                site_url=settings.SITE_URL,
                url=self.get_previous().get_absolute_url(),
            ),
            recipient=self.get_previous().author,
        )

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
                self.create_reply()
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

    def get_context_data(self, **kwargs):
        context = super(PostTaggedView, self).get_context_data(**kwargs)
        context['head'] = "Tagged Posts"
        context['lead'] = "All posts tagged with {}. Happy hunting.".format(
            self.kwargs['tag']
        )
        return context


    def get_queryset(self):
        queryset = super(PostTaggedView, self).get_queryset()
        return queryset.filter(
            tags__name=self.kwargs['tag']
        ).distinct()


class AuthoredView(PostListView):

    def get_context_data(self, **kwargs):
        context = super(AuthoredView, self).get_context_data(**kwargs)
        context['head'] = "Posts by {}".format(self.kwargs['author'])
        context['lead'] = "All posts created by {}.".format(
            self.kwargs['author']
        )
        return context

    def get_queryset(self):
        return self.model.objects.filter(
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


class PostHideView(RedirectView):

    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(models.Post, slug=self.kwargs['slug'])
        post.active = False
        post.save()
        return post.get_absolute_url()
