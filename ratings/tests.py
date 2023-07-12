from django.test import TestCase
from django.contrib.auth import get_user_model
import random
from playlists.models import Playlist
from .models import Rating, RatingChoices
# Create your tests here.
User = get_user_model()


class RatingTestCase(TestCase):
    def create_playlist(self):
        items = []
        self.playlist_count = random.randint(10, 500)

        for i in range(0, self.playlist_count):
            items.append(Playlist(title=f'TV Show{i}'))
        Playlist.objects.bulk_create(items)
        self.playlists = Playlist.objects.all()

    def create_users(self):
        items = []
        self.user_count = random.randint(10, 500)

        for i in range(0, self.user_count):
            items.append(User(username=f'user_{i}'))
        User.objects.bulk_create(items)
        self.users = User.objects.all()

    def setUp(self):
        self.create_users()
        self.create_playlist()

    def test_user_count(self):
        qs = User.objects.all()
        self.assertTrue(qs.exists())
        self.assertEqual(qs.count(), self.user_count)
        self.assertEqual(self.users.count(), self.user_count)

    def test_playlists_count(self):
        qs = Playlist.objects.all()
        self.assertTrue(qs.exists())
        self.assertEqual(qs.count(), self.playlist_count)
        self.assertEqual(self.playlists.count(), self.playlist_count)

    def create_ratings(self):
        items = []
        self.playlist_count = random.randint(10, 500)

        for i in range(0, self.user_count):
            items.append(
                Rating(
                    user=self.users.order_by("?").first(),
                    content_object=self.playlists.order_by("?").first(),
                    value=random.choice(RatingChoices.choices)[0]
                )
            )
        Rating.objects.bulk_create(items)
        self.playlists = Rating.objects.all()