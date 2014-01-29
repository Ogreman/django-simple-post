from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from vanilla import ListView, DetailView, CreateView, UpdateView
from braces.views import LoginRequiredMixin

from . import models 
from . import forms


class PostListView(ListView):
    model = models.Post


class PostDetailView(DetailView):
    model = models.Post
    lookup_field = "slug"

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        if self.object.previous:
            context['original'] = self.object.previous
        context['replies'] = self.object.post_set.are_active()
        return context    


class PostCreateView(LoginRequiredMixin, CreateView):
    model = models.Post 
    success_url = reverse_lazy('home')
    form_class = forms.PostForm

    def form_valid(self, form):
        if form.is_valid():
            if self.kwargs.get('reply', None):
                form.instance.previous = self.model.objects.get(slug=self.kwargs['reply'])
                form.save()
        return super(PostCreateView, self).form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Post
    success_url = reverse_lazy('home')    