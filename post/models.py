from django.db import models
from django.core.urlresolvers import reverse

from core.models import Content

class Post(Content):
    previous = models.ForeignKey("Post", blank=True, null=True)
    
    def get_absolute_url(self):
        return reverse("post", kwargs={"slug": self.slug})
