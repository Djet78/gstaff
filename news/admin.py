from django.contrib import admin
from django.conf import settings

from .models import Article, Comment, Complaint


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'pub_date', 'game', )
    search_fields = ('title',  'owner__login', 'game__name')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'owner', 'date_added', 'article', 'game', 'reply_to', )
    exclude = ('votes', )


class ComplainAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'date_added',)


admin.site.register(Article, ArticleAdmin)
if settings.DEBUG:
    admin.site.register(Comment, CommentAdmin)
    admin.site.register(Complaint, ComplainAdmin)
