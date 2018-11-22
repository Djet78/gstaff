from django.contrib import admin
from .models import Article, Comment


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'pub_date', 'game', )
    search_fields = ('title',  'owner__login', 'game__name')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'owner', 'add_date', 'article', 'replies', )


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
