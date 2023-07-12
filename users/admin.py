from django.contrib import admin

from .models import EmailVerification, User, VideoItem


class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('code', 'expiration')
    fields = ('code', 'expiration', 'created', 'slug')
    readonly_fields = ('created', )


admin.site.register(EmailVerification, EmailVerificationAdmin)
admin.site.register(User)
admin.site.register(VideoItem)