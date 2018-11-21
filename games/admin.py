from django.contrib import admin
from .models import Genre, Game, Studio, Platform


class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'release_date', 'studio', 'platforms_list', 'genres_list', )

    def platforms_list(self, obj):
        """ Represents platforms for particular game on admin page """
        return list(obj.platforms.all())
    platforms_list.short_description = 'Platforms'  # Admin page table name

    def genres_list(self, obj):
        """ Represents genres for particular game on admin page """
        return list(obj.genres.all())
    genres_list.short_description = 'Genres'  # Admin page table name


admin.site.register(Genre)
admin.site.register(Game, GameAdmin)
admin.site.register(Studio)
admin.site.register(Platform)
