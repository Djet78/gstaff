from django.urls import path
from .views import GameList, GameDetail, PlatformList, PlatformDetail, StudioList, StudioDetail, GenreList, GenreDetail

app_name = 'games'

urlpatterns = [
    path('games/', GameList.as_view(), name='game_list'),
    path('games/<name>/', GameDetail.as_view(), name='game_detail'),
    path('platforms/', PlatformList.as_view(), name='platform_list'),
    path('platforms/<name>/', PlatformDetail.as_view(), name='platform_detail'),
    path('studios/', StudioList.as_view(), name='studio_list'),
    path('studios/<name>/', StudioDetail.as_view(), name='studio_detail'),
    path('genres/', GenreList.as_view(), name='genre_list'),
    path('genres/<name>/', GenreDetail.as_view(), name='genre_detail'),
]
