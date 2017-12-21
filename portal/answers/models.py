from django.db import models
from django.conf import settings
from portal.utils import unique_slug_generator
from django.urls import reverse
from django.db.models import Q
from django.db.models.signals import pre_save

# Create your models here.
User = settings.AUTH_USER_MODEL


class PublicContribQuerySet(models.QuerySet):
    def search(self, query):
        if query:
            query = query.strip()
            return self.filter(
                Q(exid__icontains=query) |
                Q(exid__iexact=query) |
                Q(shortname__icontains=query) |
                Q(shortname__iexact=query)
            ).distinct()
        return self


class PublicContribManager(models.Manager):
    def get_queryset(self):
        return PublicContribQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)


class PublicContrib(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    shortname = models.CharField(max_length=32)
    exid = models.CharField(max_length=16, null=True)
    desc = models.CharField(max_length=64, null=True)
    slug = models.SlugField(null=True, blank=True)
    ispublic = models.BooleanField(default=False)
    popularity = models.IntegerField(default=0)

    objects = PublicContribManager()

    def get_absolute_url(self):
        return reverse('answers:get', kwargs={'slug': self.slug})

    def get_absolute_url_edit(self):
        return reverse('answers:edit', kwargs={'slug': self.slug})

    def __str__(self):
        return self.shortname

    @property
    def title(self):
        return self.exid


def pc_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(pc_pre_save_receiver, sender=PublicContrib)
