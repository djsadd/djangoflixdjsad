# Generated by Django 4.2 on 2023-07-14 09:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0002_playlist_poster'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playlist',
            old_name='poster',
            new_name='img',
        ),
    ]
