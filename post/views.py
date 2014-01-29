from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse_lazy

from vanilla import ListView, DetailView, CreateView, UpdateView
from braces.views import LoginRequiredMixin
from core import views as core_views

from . import models 
from . import forms


class PostListView(ListView):
    model = models.Post

    def get_queryset(self):
        return self.model.objects.originals().are_active()


class PostDetailView(core_views.TagsContextMixin, DetailView):
    model = models.Post
    lookup_field = "slug"

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        if self.object.previous:
            context['original'] = self.object.previous
        context['replies'] = self.object.post_set.are_active()
        return context    


class PostCreateView(LoginRequiredMixin, core_views.AuthoredMixin, CreateView):
    
    model = models.Post 
    success_url = reverse_lazy('home')
    form_class = forms.PostForm

    def get_previous(self):
        if not hasattr(self, "previous"):
            self.previous = get_object_or_404(self.model, slug=self.kwargs['reply'])
        return self.previous

    def get_context_data(self, **kwargs):
        context = super(PostCreateView, self).get_context_data(**kwargs)
        if self.kwargs.get('reply', None):
            context['previous'] = self.get_previous()
        return context    

    def form_valid(self, form):
        if form.is_valid():
            if self.kwargs.get('reply', None):
                form.instance.previous = self.get_previous()
                form.save()
        return super(PostCreateView, self).form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Post
    success_url = reverse_lazy('home')    