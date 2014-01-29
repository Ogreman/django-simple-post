from django.db import models


class ContentQuerySet(models.query.QuerySet):

    def are_active(self):
        return self.filter(active=True)


class ContentManager(models.Manager):

    def get_query_set(self):
        return ContentQuerySet(self.model, using=self._db)

    def are_active(self):
        return self.get_query_set().are_active()
