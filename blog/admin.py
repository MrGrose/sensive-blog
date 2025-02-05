from django.contrib import admin
from blog.models import Post, Tag, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    raw_id_fields = ('tags',)
    list_display = ('title', 'text', 'slug', 'image', 'published_at', 'author',)
    list_select_related = ('author',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    raw_id_fields = ('post',)
    list_display = ('post', 'author', 'text', 'published_at')
    list_select_related = ('post', 'author')
