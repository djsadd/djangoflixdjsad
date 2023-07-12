from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models.signals import pre_save

from DjangoFLix.db.utils import get_unique_slug
# Create your models here.
from tags.models import TaggedItem


class Category(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    tags = GenericRelation(TaggedItem, related_query_name='category')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return f"/category/{self.slug}/"


def unique_slugify_pre_save(sender, instance, *args, **kwargs):
    title = instance.title
    slug = instance.slug
    if slug is None:
        instance.slug = get_unique_slug(instance, size=5)


pre_save.connect(unique_slugify_pre_save, sender=Category)