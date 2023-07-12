from playlists.models import *
from .models import *

video_a = Video.objects.create(title='My video', video_id='asd')
obj_a = Playlist.objects.create(title='This is my title', video=video_a)
