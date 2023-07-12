
class PlaylistMixin():
    title = None
    template_name = 'playlists/playlist_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["title"] = self.title
        return context

    def get_queryset(self):
        qs = super().get_queryset().order_by('compilation')
        print(qs, "SBDHSBDKJASBDKJASKD")
        return qs[::-1]
