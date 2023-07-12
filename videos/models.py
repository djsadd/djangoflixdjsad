from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import pre_save


# Create your models here.


class VideoQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(
            state=PublishStateOptions.PUBLISHED,
            publish_time_stamp__lte=now
        )


class VideoManager(models.Manager):
    def get_queryset(self):
        return VideoQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()


class PublishStateOptions(models.TextChoices):
    # CONSTANT = DB_VALUE , USER DISPLAY UA
    PUBLISHED = 'PU', 'Publish'
    DRAFT = 'DR', 'Draft'
    # UNLISTED = 'UB', 'UNLISTED'
    # PRIVATE = 'PR', 'PRIVATE'


class Video(models.Model):
    VideoStateOptions = PublishStateOptions
    title = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    video_id = models.CharField(max_length=30, unique=True)
    active = models.BooleanField(default=True)
    time_stamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=2, choices=VideoStateOptions.choices, default=VideoStateOptions.DRAFT)
    publish_time_stamp = models.DateTimeField(auto_now_add=False, auto_now=True, blank=True, null=True)
    video = models.FileField(null=True, blank=True)
    poster = models.ImageField(null=True, blank=True)

    objects = VideoManager()

    def get_video_id(self):
        if not self.is_published:
            return None
        return self.video_id

    @property
    def is_published(self):
        if self.active is False:
            return False
        state = self.state
        if state != PublishStateOptions.PUBLISHED:
            return False
        pub_timestamp = self.publish_time_stamp
        return True

    def time_stamp(self):
        return self.publish_time_stamp

    def get_playlist_ids(self):
        return list(self.playlist_set.all().values_list('id', flat=True))

    def __str__(self):
        return f"{self.title}"


class VideoProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'Published Videos'
        verbose_name_plural = 'Published Videos'


class VideoAllProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'All Videos'
        verbose_name_plural = 'All Videos'


def publish_state_pre_save(sender, instance, *args, **kwargs):
    if instance.state == PublishStateOptions.PUBLISHED and instance.publish_time_stamp is None:
        instance.publish_time_stamp = timezone.now()
    elif instance.state == PublishStateOptions.DRAFT:
        instance.publish_time_stamp = None


pre_save.connect(publish_state_pre_save, sender=Video)


def slugify_pre_save(sender, instance, *args, **kwargs):
    title = instance.title
    slug = instance.slug
    if slug is None:
        instance.slug = slugify(title)


pre_save.connect(slugify_pre_save, sender=Video)


pre_save.connect(publish_state_pre_save, sender=VideoProxy)
pre_save.connect(slugify_pre_save, sender=VideoProxy)

pre_save.connect(publish_state_pre_save, sender=VideoAllProxy)
pre_save.connect(slugify_pre_save, sender=VideoAllProxy)
