from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.http import Http404, StreamingHttpResponse

from users.models import VideoItem
from videos.models import Video
from .mixins import PlaylistMixin

# Create your views here.
from .models import MovieProxy, TVShowProxy, Playlist, TVShowSeasonProxy, Comp, MenuChoices, CompChoices
from .models import PublishStateOptions
from .services import open_file


class SearchView(PlaylistMixin, ListView):
    template_name = 'playlists/search.html'

    def get_context_data(self, *args, **kwargs):
        query = self.request.GET.get('q')
        context = super(SearchView, self).get_context_data(*args, **kwargs)
        if query:
            context['title'] = f"Searched for {query}"
        else:
            context['title'] = f"Perform a search"
        return context

    def get_queryset(self):
        print('qeury')
        request = self.request
        query = request.GET.get('q')
        print(Playlist.objects.all().movie_or_show().search(query=query))
        return Playlist.objects.all().movie_or_show().search(query=query)


class MovieListView(PlaylistMixin, ListView):
    template_name = 'playlists/movies.html'
    queryset = Comp.objects.filter(menuchoices=MenuChoices.MOVIE)
    title = "Movies"


class MovieDetailView(PlaylistMixin, DetailView):
    template_name = 'playlists/movie_detail.html'
    queryset = MovieProxy.objects.all()


class PlaylistDetailView(PlaylistMixin, DetailView):
    template_name = 'playlists/playlist_detail.html'
    queryset = Playlist.objects.all()


class TVShowDetailView(PlaylistMixin, DetailView):
    template_name = 'playlists/tv_show_detail.html'
    queryset = TVShowProxy.objects.all()


class TVShowSeasonDetailView(PlaylistMixin, DetailView):
    template_name = 'playlists/season_detail.html'
    queryset = TVShowSeasonProxy.objects.all()

    def get_object(self, queryset=None):
        kwargs = self.kwargs
        show_slug = kwargs['slug']
        season_slug = kwargs['seasonSlug']
        now = timezone.now()
        try:
            obj = TVShowSeasonProxy.objects.get(
                state=PublishStateOptions.PUBLISHED,
                publish_time_stamp__lte=now,
                parent__slug__iexact=show_slug,
                slug__iexact=season_slug,
            )
        except TVShowSeasonProxy.MultipleObjectsReturned:
            qs = TVShowSeasonProxy.objects.filter(
                parent__slug__iexact=show_slug,
                slug__iexact=season_slug,
            ).publised()
            obj = qs.first()
        except:
            raise Http404

        return obj


class TVShowProxyListView(PlaylistMixin, ListView):
    template_name = 'playlists/tvshow.html'
    queryset = Comp.objects.filter(menuchoices=MenuChoices.TVSHOW)
    title = "TV Show"


class FeaturedPlaylistListView(PlaylistMixin, ListView):
    template_name = 'playlists/featured_list.html'
    queryset = Video.objects.all()
    title = "Featured"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={"object_list": VideoItem.objects.filter(user=request.user)})


class HomePageListView(PlaylistMixin, ListView):
    template_name = 'playlists/home_page.html'
    queryset = Comp.objects.filter(menuchoices=MenuChoices.HOME)
    title = "Home"

    def get_context_data(self, *args, **kwargs):
        context = super(HomePageListView, self).get_context_data(*args, **kwargs)
        context['title'] = self.title
        return context


def get_episode(request, pk, season_pk, episode_pk):
    return get_serial(request, pk, season_pk, episode_pk)


def get_season(request, pk, season_pk):
    return get_serial(request, pk, season=season_pk)


def get_video(request, pk):
    playlist = Playlist.objects.get(pk=pk)
    print(playlist)
    _video = get_object_or_404(Video, id=playlist.video.pk)
    print(_video)
    return render(request, "playlists/video.html", {"playlist": playlist, "video": _video})


def get_serial(request, pk, season=None, episode=None):
    tv_show = TVShowProxy.objects.get(pk=pk)
    print(tv_show)
    seasons = tv_show.get_seasons()
    if season is None and episode is None:
        episodes = seasons[0].videos.all()
        episode = episodes[0]
        return render(request, 'playlists/video_series.html', {"video": episode, 'seasons': seasons, 'episodes': episodes, "tv_show": tv_show, 'season': seasons[0]})
    season = tv_show.get_seasons(season=season)
    episodes = season.videos.all()
    if episode is None:
        episode = episodes[0]
    else:
        episode = episodes.filter(pk=episode)[0]
        print(episode)
    return render(request, "playlists/video_series.html", {"video": episode, 'seasons': seasons, 'episodes': episodes, "tv_show": tv_show, 'season': season})


def get_streaming_video(request, playlist, pk):
    _video = get_object_or_404(Video, id=pk)
    videos = VideoItem.objects.filter(user=request.user, video=Video.objects.get(pk=pk)).last()
    if videos:
        file, status_code, content_length, content_range, video = open_file(request, pk)
    else:
        VideoItem.objects.create(user=request.user, video=_video, time='0', playlist=Playlist.objects.get(pk=playlist))
        file, status_code, content_length, content_range, video = open_file(request, pk)

    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')
    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response
