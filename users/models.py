from django.conf import settings
from django.db import models
# Create your models here.
from django.core.mail import send_mail
from django.db.models.signals import pre_save
from django.utils.timezone import now
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from videos.models import Video
from playlists.models import Playlist
from datetime import datetime


class User(AbstractUser):

    class AgeRatingChoice(models.TextChoices):
        BABY = "BABY"
        TEEN = "TEEN"
        OLD = "OLD"

    image = models.ImageField(upload_to='users/images', null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)
    slug = models.SlugField(blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    age = models.IntegerField(null=True, blank=True)
    date_birthday = models.DateField(null=True, blank=True)
    children = models.ManyToManyField("self", null=True, blank=True)
    rate = models.CharField(max_length=4, choices=AgeRatingChoice.choices, default=AgeRatingChoice.TEEN)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        context = super(User, self).save(*args, **kwargs)
        # self.age = now().date()-self.date_birthday
        # print(self.age)
        return context

    def get_children(self):
        return self.children.all()

    def remove_children(self):
        self.delete()


class VideoItem(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    video = models.ForeignKey(to=Video, on_delete=models.CASCADE)
    time = models.CharField(max_length=100, null=True, blank=True)
    playlist = models.ForeignKey(to=Playlist, on_delete=models.SET_NULL, blank=True, null=True)


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True, null=True, blank=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, default=now)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField(null=True, blank=True)

    # def __str__(self):
    #     return f"Email verification {self.user.email}"

    def send_verification_email(self):
        link = reverse('verify', kwargs={'email': self.user.email, 'code': self.code})
        send_mail(
            subject='Подтвердите адрес электронной почты',
            message=f'Для подтвреждения адреса электронной почты перейдите по ссылке: {settings.DOMAIN_NAME}{link}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return now() >= self.expiration


def slugify_pre_save(sender, instance, *args, **kwargs):
    username = instance.username
    slug = instance.slug
    if slug is None:
        instance.slug = slugify(username)


pre_save.connect(slugify_pre_save, sender=User)
