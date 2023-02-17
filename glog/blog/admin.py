from django.contrib import admin
from .models import Post, Comment

# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['blog_title', 'author', 'date_published', 'status', 'tags']
    list_filter = ['author', 'date_created', 'status', 'tags']
    prepopulated_fields = {'blog_slug_title': ('blog_title',)}
    date_hierarchy = 'date_published'
    search_fields = ['blog_title', 'body']
    raw_id_fields = ['author']
    list_per_page = 3
    ordering = ['status', 'date_published']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'post', 'user_img']
