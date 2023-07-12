from django.db import models
from django.db.models import Avg, Max, Min, Q
from django.contrib.contenttypes.fields import GenericRelation
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import pre_save

from videos.models import Video
from categories.models import Category
# Create your models here.
from tags.models import TaggedItem
from ratings.models import Rating
from DjangoFLix.db.utils import get_unique_slug


class PlaylistQuerySet(models.QuerySet):
    def published(self):
        return self.filter(
            state=PublishStateOptions.PUBLISHED,
        )

    def movie_or_show(self):
        return self.filter(
            Q(tp=Playlist.PlaylistTypeChoices.MOVIE) |
            Q(tp=Playlist.PlaylistTypeChoices.SHOW)
        )

    def search(self, query):
        if query is None:
            return self.none()
        return self.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__title__icontains=query) |
            Q(category__slug__icontains=query) |
            Q(tags__tag__icontains=query),
        )


class PlaylistManager(models.Manager):
    def get_queryset(self):
        return PlaylistQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def featured_playlists(self):
        return self.get_queryset().filter(tp=Playlist.PlaylistTypeChoices.PLAYLIST)


class PublishStateOptions(models.TextChoices):
    # CONSTANT = DB_VALUE , USER DISPLAY UA
    PUBLISHED = 'PU', 'Publish'
    DRAFT = 'DR', 'Draft'
    # UNLISTED = 'UB', 'UNLISTED'
    # PRIVATE = 'PR', 'PRIVATE'


class Playlist(models.Model):
    class PlaylistTypeChoices(models.TextChoices):
        MOVIE = 'MOV', "Movie"
        SHOW = 'TV', 'TV Show'
        SEASON = 'SEA', 'Season'
        PLAYLIST = 'PLY', 'Playlist'

    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL, related_name='playlists')
    VideoStateOptions = PublishStateOptions
    order = models.IntegerField(default=1)
    related = models.ManyToManyField("self", blank=True, related_name='related', through='PlaylistRelated')
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=220)
    tp = models.CharField(max_length=3, choices=PlaylistTypeChoices.choices, default=PlaylistTypeChoices.PLAYLIST)
    description = models.TextField(blank=True, null=True)
    video = models.ForeignKey(to=Video, blank=True, null=True, on_delete=models.SET_NULL)
    videos = models.ManyToManyField(Video, related_name='playlist_item', blank=True, through='PlaylistItem')
    slug = models.SlugField(blank=True, null=True)
    active = models.BooleanField(default=True)
    time_stamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=2, choices=VideoStateOptions.choices, default=VideoStateOptions.DRAFT)
    publish_time_stamp = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
    tags = GenericRelation(TaggedItem, related_query_name='playlist')
    rating = GenericRelation(Rating, related_query_name='playlist')
    age_limit = models.CharField(max_length=3, blank=True, null=True)
    posters = models.ImageField(upload_to='photos/%Y/%m/%d/', null=True, blank=True)
    logo = models.ImageField(upload_to='photos/%Y/%m/%d/', null=True, blank=True)
    trailer = models.FileField(null=True, blank=True)

    objects = PlaylistManager()

    def __str__(self):
        return self.title

    def get_seasons(self, season=None):
        if season is None:
            return self.playlist_set.all()
        else:
            print(season)
            for row in self.playlist_set.all():
                print(row, row.id)
            return self.playlist_set.get(pk=season)

    def get_episodes(self, episode=None):
        if episode is None:
            return self.videos.all()[0]
        else:
            return self.videos.all()

    def get_absolute_url(self):
        if self.is_movie:
            return f'/movies/{self.slug}/'
        elif self.is_show:
            return f'/shows/{self.slug}/'

        elif self.is_season and self.parent is not None:
            return f'/shows/{self.parent.slug}/seasons/{self.slug}/'

        return f"/playlists/{self.slug}"

    def get_related_items(self):
        qs = self.playlistrelated_set.all()
        return self.playlistrelated_set.all()

    @property
    def is_movie(self):
        return self.tp == Playlist.PlaylistTypeChoices.MOVIE

    @property
    def is_season(self):
        return self.tp == Playlist.PlaylistTypeChoices.SEASON

    def get_count_episodes(self):
        return f"{self.playlist_set.all().count()} seasons"

    @property
    def is_show(self):
        return self.tp == Playlist.PlaylistTypeChoices.SHOW

    @property
    def is_published(self):
        return self.active

    def time_stamp(self):
        return None

    def get_avg_rating(self):
        return Playlist.objects.filter(id=self.id).aggregate(Avg("rating__value"))

    def get_spread_rating(self):
        return Playlist.objects.filter(id=self.id).aggregate(max=Max("rating__value"), min=Min("rating__value"))

    def get_short_display(self):
        return f""

    def get_video_id(self):
        if self.video is None:
            return None
        return self.video.get_video_id()

    def get_clips(self):
        return self.playlistitem_set.all().published()


def publish_state_pre_save(sender, instance, *args, **kwargs):
    if instance.state == PublishStateOptions.PUBLISHED and instance.publish_time_stamp is None:
        instance.publish_time_stamp = timezone.now()
    elif instance.state == PublishStateOptions.DRAFT:
        instance.publish_time_stamp = None


pre_save.connect(publish_state_pre_save, sender=Playlist)


def slugify_pre_save(sender, instance, *args, **kwargs):
    title = instance.title
    slug = instance.slug
    if slug is None:
        instance.slug = slugify(title)


def unique_slugify_pre_save(sender, instance, *args, **kwargs):
    title = instance.title
    slug = instance.slug
    if slug is None:
        instance.slug = get_unique_slug(instance, size=5)


pre_save.connect(unique_slugify_pre_save, sender=Playlist)


class PlaylistItemQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()

        return self.filter(
            playlist__state=PublishStateOptions.PUBLISHED,
            video__state=PublishStateOptions.PUBLISHED,
        )


class PlaylistItemManager(models.Manager):
    def get_queryset(self):
        return PlaylistItemQuerySet(self.model, using=self._db)

    def published(self):
        return self.PlaylistItemQuerySet(self.model, using=self._db).published()


def pr_limit_choices_to():
    return Q(tp=Playlist.PlaylistTypeChoices.MOVIE, state=Playlist.VideoStateOptions.PUBLISHED) | Q(tp=Playlist.PlaylistTypeChoices.SHOW, state=Playlist.VideoStateOptions.PUBLISHED)


class PlaylistRelated(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    related = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name="related_item", limit_choices_to=pr_limit_choices_to)
    order = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)


class PlaylistItem(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = PlaylistItemManager()

    class Meta:
        ordering = ['order', '-timestamp']


class TVShowProxyManager(models.Manager):
    def get_queryset(self):
        return PlaylistQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().filter(parent__isnull=True, tp=Playlist.PlaylistTypeChoices.SHOW)


class TVShowProxy(Playlist):
    objects = TVShowProxyManager()

    class Meta:
        proxy = True
        verbose_name = 'TV Show'
        verbose_name_plural = 'TV Shows'

    def save(self, *args, **kwargs):
        self.tp = Playlist.PlaylistTypeChoices.SHOW
        super(TVShowProxy, self).save(*args, **kwargs)

    def seasons(self):
        return self.playlist_set.all()

    def get_short_display(self):
        return f"{self.playlist_set.all().count()} seasons"

    def get_video_id(self):
        if self.video is None:
            return None
        return self.video.get_video_id()

    def get_clips(self):
        return self.playlistitem_set.all().published()


class MovieProxyManager(models.Manager):
    def get_queryset(self):
        return PlaylistQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().filter(tp=Playlist.PlaylistTypeChoices.MOVIE)


class MovieProxy(Playlist):
    objects = MovieProxyManager()

    def get_movie_id(self):
        return self.get_video_id()

    class Meta:
        proxy = True
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'

    def save(self, *args, **kwargs):
        self.tp = Playlist.PlaylistTypeChoices.MOVIE
        super(MovieProxy, self).save(*args, **kwargs)


class TVShowSeasonProxyManager(models.Manager):

    def get_queryset(self):
        return PlaylistQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().filter(parent__isnull=False, tp=Playlist.PlaylistTypeChoices.SEASON)


class TVShowSeasonProxy(Playlist):
    objects = TVShowSeasonProxyManager()

    class Meta:
        proxy = True
        verbose_name = 'Season'
        verbose_name_plural = 'Seasons'

    def save(self, *args, **kwargs):
        self.tp = Playlist.PlaylistTypeChoices.SEASON
        super(TVShowSeasonProxy, self).save(*args, **kwargs)

    def get_episodes(self):
        return self.playlistitem_set.all().published()

    def get_season_trailer(self):
        return self.get_video_id


class MenuChoices(models.TextChoices):
    HOME = 'HM', "Home"
    TVSHOW = 'TV', 'TVShow'
    MOVIE = 'MOV', 'MOVIE'


class CompChoices(models.TextChoices):
    BIGCOMPILATION = 'BIG', "BigCompOne"
    COMPILATION = 'CP', 'Compilation'
    HeadCompilation = 'HC', 'HeadCompilation'


class Comp(models.Model):

    title = models.CharField(max_length=128)
    pla = models.ManyToManyField(Playlist)
    compilation = models.CharField(max_length=3, choices=CompChoices.choices, default=CompChoices.COMPILATION)
    menuchoices = models.CharField(max_length=3, choices=MenuChoices.choices, default=MenuChoices.HOME)

    def is_compilation(self):
        return self.compilation == CompChoices.COMPILATION

    def is_bigcompilation(self):
        return self.compilation == CompChoices.BIGCOMPILATION

    def is_header(self):
        return self.compilation == CompChoices.HeadCompilation

    def get_playlist(self):
        return self.pla.all()

    def get_show(self):
        return self.pla.all()[0]

    def __str__(self):
        return f"{self.title} | {self.menuchoices} | {self.compilation}"

    def order(self):
        return self.pla.objects.all()


pre_save.connect(publish_state_pre_save, sender=TVShowProxy)
pre_save.connect(unique_slugify_pre_save, sender=TVShowProxy)

pre_save.connect(publish_state_pre_save, sender=MovieProxy)
pre_save.connect(unique_slugify_pre_save, sender=MovieProxy)

pre_save.connect(publish_state_pre_save, sender=TVShowSeasonProxy)
pre_save.connect(unique_slugify_pre_save, sender=TVShowSeasonProxy)
