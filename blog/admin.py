from django.contrib import admin
from blog.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie_title', 'movie_rating',
                    'comment', 'modify_dt')
    list_editable = ('movie_title', 'movie_title',
                     'movie_rating', 'comment')
    list_filter = ('modify_dt',)
