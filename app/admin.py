from django.contrib import admin
from .models import Topic, Video


class VideoInline(admin.TabularInline):
    model = Video
    extra = 1


class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    inlines = [VideoInline]


admin.site.register(Topic, TopicAdmin)

admin.site.register(Video)
