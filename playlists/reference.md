the_office = Playlist.objects.create(title='The office series')

season_1 = Playlist.objects.create(title='The office season 1', parent=the_office, order=1)

season_2 = Playlist.objects.create(title='The office season 2', parent=the_office, order=2)

season_2 = Playlist.objects.create(title='The office season 3', parent=the_office, order=3)

shows = Playlist.objects.filter(parent__isnull=True)
show = Playlist.objects.get(id=1)