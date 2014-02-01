from django.db import models
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage
from django.conf import settings

from core.models import Content, TimeStampedModel

from . import managers


class Post(Content):

    previous = models.ForeignKey("Post", blank=True, null=True)
    objects = managers.PostManager()

    def get_absolute_url(self):
        return reverse("post", kwargs={"slug": self.slug})

    @property
    def replies(self):
        return self.post_set.order_by('created')


class Email(TimeStampedModel):

	subject = models.CharField(max_length=255, blank=True)
	content = models.TextField(blank=True)
	recipient = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		related_name="all_mail",
		blank=True,
	 	null=True
 	)
	sent = models.BooleanField(default=False)

	def send(self):
		msg = EmailMessage(self.subject, self.content, settings.DEFAULT_FROM_EMAIL, [self.recipient.email])
		msg.content_subtype = "html"
		msg.send()
		self.sent = True
		self.save()


