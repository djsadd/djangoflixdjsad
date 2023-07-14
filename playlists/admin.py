from django.contrib import admin
# Register your models here.
from .models import Playlist, PlaylistItem, TVShowProxy, TVShowSeasonProxy, MovieProxy,PlaylistRelated, Comp
from tags.admin import TagItemInline


class MovieProxyAdmin(admin.ModelAdmin):
    inlines = [TagItemInline]
    list_display = ['title']
    fields = ['title', 'description', 'category', 'state', 'video', 'slug', 'age_limit', 'posters', 'logo', 'trailer', 'img']

    class Meta:
        model = MovieProxy

    def get_queryset(self, request):
        return MovieProxy.objects.all()


admin.site.register(MovieProxy, MovieProxyAdmin)


class SeasonEpisodeInline(admin.TabularInline):
    model = PlaylistItem
    extra = 0


class TVShowSeasonProxyAdmin(admin.ModelAdmin):
    inlines = [SeasonEpisodeInline]
    list_display = ['title', 'parent']

    class Meta:
        model = TVShowSeasonProxy

    def get_queryset(self, request):
        return TVShowSeasonProxy.objects.all()


admin.site.register(TVShowSeasonProxy, TVShowSeasonProxyAdmin)


class TVShowSeasonProxyInline(admin.TabularInline):
    extra = 0
    model = TVShowSeasonProxy
    fields = ['order', 'title', 'state']


class TVShowProxyAdmin(admin.ModelAdmin):
    inlines = [TagItemInline, TVShowSeasonProxyInline]
    fields = ['title', 'description', 'category', 'state', 'video', 'slug', 'age_limit', 'posters', 'logo', 'trailer', 'img']
    list_display = ['title', 'posters']

    class Meta:
        model = TVShowProxy

    def get_queryset(self, request):
        return TVShowProxy.objects.all()


admin.site.register(TVShowProxy, TVShowProxyAdmin)


class PlaylistRelatedInline(admin.TabularInline):
    model = PlaylistRelated
    fk_name = 'playlist'
    extra = 0


class PlaylistItemInline(admin.TabularInline):
    model = PlaylistItem
    extra = 0


class PlaylistAdmin(admin.ModelAdmin):
    inlines = [PlaylistRelatedInline, PlaylistItemInline]
    fields = [
        'title', 'description', 'slug', 'state', 'active'
    ]

    class Meta:
        model = Playlist

    def get_queryset(self, request):
        return Playlist.objects.filter(tp=Playlist.PlaylistTypeChoices.PLAYLIST)


admin.site.register(Playlist, PlaylistAdmin)


class MovieProxyCompInlines(admin.TabularInline):
    model = Comp.pla.through
    extra = 0


class CompAdmin(admin.ModelAdmin):
    inlines = [
        MovieProxyCompInlines
    ]
    fields = [
        'title', 'compilation', 'menuchoices'
    ]


admin.site.register(Comp, CompAdmin)
