from django.shortcuts import render
from django.views.generic import ListView, DetailView
from playlists.models import Playlist
from django.db.models import Count
from .models import Category
from playlists.mixins import PlaylistMixin


class CategoryListView(ListView):
    template_name = 'categories/category_list.html'
    queryset = Category.objects.all().filter(active=True).annotate(pl_count=Count('playlists')).filter(pl_count__gt=0)


class CategoryDetailView(PlaylistMixin, ListView):
    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
        obj = Category.objects.get(slug=self.kwargs['slug'])
        context['object'] = obj
        if obj is not None:
            context['title'] = obj.title
        return context

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return Playlist.objects.filter(category__slug=slug, state=Playlist.VideoStateOptions.PUBLISHED).movie_or_show()