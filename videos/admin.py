from django.contrib import admin
from .models import Video, VideoProxy, VideoAllProxy
# Register your models here.


class VideoAllAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'state', 'video_id', 'is_published', 'get_playlist_ids', 'publish_time_stamp']
    search_fields = ['title']
    list_filter = ['state', 'active']
    readonly_fields = ['id', 'is_published', 'get_playlist_ids']

    class Meta:
        model = Video


class VideoProxyAdmin(admin.ModelAdmin):
    list_display = ['title', 'video_id']
    search_fields = ['title']
    # list_filter = ['video_id']

    class Meta:
        model = VideoAllProxy

    def get_queryset(self, request):
        return VideoProxy.objects.filter(active=True)


admin.site.register(VideoAllProxy, VideoAllAdmin)
admin.site.register(VideoProxy, VideoProxyAdmin)
