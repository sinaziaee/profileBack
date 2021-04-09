from django.contrib import admin
from post.models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ['post_id', 'title', 'description', 'sender', 'dateTime']
    search_fields = ['post_id', 'title', 'description', 'sender']
    list_filter = ['post_id', 'sender', 'title']

    def post_title(self, obj):
        result = Post.objects.get(post_id=obj.id)
        return result.title

    def post_sender(self, obj):
        result = Post.objects.get(post_id=obj.id)
        return result.sender

    class Meta:
        model = Post


admin.site.register(Post, PostAdmin)
