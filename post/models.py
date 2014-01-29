from django.db import models
from django.core.urlresolvers import reverse

from core.models import Content

from . import managers

class Post(Content):

    previous = models.ForeignKey("Post", blank=True, null=True)
    objects = managers.PostManager()
    
    def get_absolute_url(self):
        return reverse("post", kwargs={"slug": self.slug})
