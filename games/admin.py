from django.contrib import admin

from .models import Genre, Game, Studio, Platform, Publisher


class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'release_date', 'studio', 'platforms_list', 'genres_list', )
    search_fields = ('name', 'platforms__name', 'genres__name', 'studio__name', )

    def platforms_list(self, obj):
        """ Represents platforms for particular game on admin page """
        return list(obj.platforms.values_list('name', flat=True))
    platforms_list.short_description = 'Platforms'  # Admin page table name

    def genres_list(self, obj):
        """ Represents genres for particular game on admin page """
        return list(obj.genres.values_list('name', flat=True))
    genres_list.short_description = 'Genres'  # Admin page table name


admin.site.register(Game, GameAdmin)
admin.site.register(Genre)
admin.site.register(Platform)
admin.site.register(Publisher)
admin.site.register(Studio)
