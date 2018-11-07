from django.contrib import admin
from .models import Genre, Game, Studio, Platform


admin.site.register(Genre)
admin.site.register(Game)
admin.site.register(Studio)
admin.site.register(Platform)
