from django.urls import path
from .views import GameList, GameDetail, PlatformList, PlatformDetail, StudioList, StudioDetail, GenreList, GenreDetail

app_name = 'games'

urlpatterns = [
    path('games/', GameList.as_view(), name='game_list'),
    path('games/<int:pk>/', GameDetail.as_view(), name='game_detail'),
    path('platforms/', PlatformList.as_view(), name='platform_list'),
    path('platforms/<int:pk>/', PlatformDetail.as_view(), name='platform_detail'),
    path('studios/', StudioList.as_view(), name='studio_list'),
    path('studios/<int:pk>/', StudioDetail.as_view(), name='studio_detail'),
    path('genres/', GenreList.as_view(), name='genre_list'),
    path('genres/<int:pk>/', GenreDetail.as_view(), name='genre_detail'),
]
