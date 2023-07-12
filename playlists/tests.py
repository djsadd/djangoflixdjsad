from django.test import TestCase
from playlists.models import *
from django.utils import timezone
# Create your tests here.


class PlaylistModelTestCase(TestCase):
    def setUp(self):
        self.video_a = Video.objects.create(title='My video', video_id='asd')
        self.obj_a = Playlist.objects.create(title='This my title', video=self.video_a)
        self.obj_b = Playlist.objects.create(title='Title', state=PublishStateOptions.PUBLISHED, video=self.video_a)

    def test_video_playlist(self):
        qs = self.video_a.playlist_set.all()
        self.assertEqual(qs.count(), 2)

    def test_playlist_video(self):
        self.assertEqual(self.obj_a.video, self.video_a)

    def test_valid_title(self):
        title = 'This my title'
        qs = Playlist.objects.filter(title=title)
        self.assertTrue(qs.exists())

    def test_equal_count(self):
        qs = Playlist.objects.all()
        self.assertEqual(qs.count(), 2)

    def test_draft_case(self):
        qs = Playlist.objects.filter(state=PublishStateOptions.DRAFT)
        self.assertEqual(qs.count(), 1)

    def test_publish_case(self):
        qs = Playlist.objects.filter(state=PublishStateOptions.PUBLISHED)
        now = timezone.now()
        published_qs = Playlist.objects.filter(
            state=PublishStateOptions.PUBLISHED,
            publish_time_stamp__lte=now
        )
        self.assertEqual(qs.count(), 1)
        self.assertTrue(published_qs.exists())

    def test_slug_field(self):
        title = self.obj_a.title
        test_slug = slugify(title)
        self.assertEqual(test_slug, self.obj_a.slug)
