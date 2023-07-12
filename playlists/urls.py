"""
URL configuration for DjangoFLix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import *
from ratings.views import rate_object_view

urlpatterns = [
    path('movies/', MovieListView.as_view(), name='movies'),
    path('movies/<slug:slug>/', MovieDetailView.as_view(), name='movie_detail'),

    path('shows/', TVShowProxyListView.as_view(), name='shows'),
    path('shows/<slug:slug>/', TVShowDetailView.as_view(), name='show'),
    path('shows/<slug:slug>/seasons/', TVShowDetailView.as_view(), name='show_seasons'),
    path('shows/<slug:slug>/seasons/<slug:seasonSlug>/', TVShowSeasonDetailView.as_view(), name='show_season'),

    path('search/', SearchView.as_view(), name='search'),

    path('featured/', FeaturedPlaylistListView.as_view(), name='featured'),
    path('featured/media/<int:pk>/', PlaylistDetailView.as_view(), name='featured_playlist'),
    path('object-rate/', rate_object_view, name='rating'),
    path('home/', HomePageListView.as_view(), name='home'),

    path('stream/<int:playlist>/<int:pk>/', get_streaming_video, name='stream'),
    path('video/<int:pk>/', get_video, name='video'),
    path('video_serial/<int:pk>/', get_serial, name='serial'),
    path('season/<int:pk>/<int:season_pk>/', get_season, name='season'),
    path('season/<int:pk>/<int:season_pk>/<int:episode_pk>/', get_episode, name='episode'),
]
