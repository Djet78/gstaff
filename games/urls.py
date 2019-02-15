from django.urls import path
from .views import (
    GameList, GameDetail,
    GenreList, GenreDetail,
    PlatformList, PlatformDetail,
    StudioList, StudioDetail,
    ObjectCreate, ObjectChange, ObjectDelete
)

app_name = 'games'

# TODO Make urls cleaner (place dependent urls into include())
urlpatterns = [
    path('games/', GameList.as_view(), name='game_list'),
    path('games/<name>/', GameDetail.as_view(), name='game_detail'),
    path('platforms/', PlatformList.as_view(), name='platform_list'),
    path('platforms/<name>/', PlatformDetail.as_view(), name='platform_detail'),
    path('studios/', StudioList.as_view(), name='studio_list'),
    path('studios/<name>/', StudioDetail.as_view(), name='studio_detail'),
    path('genres/', GenreList.as_view(), name='genre_list'),
    path('genres/<name>/', GenreDetail.as_view(), name='genre_detail'),
    path('<instance_name>/add/', ObjectCreate.as_view(), name='games_object_crete'),
    path('<instance_name>/<slug>/change/', ObjectChange.as_view(), name='games_object_change'),
    path('<instance_name>/<slug>/delete/', ObjectDelete.as_view(), name='games_object_delete'),

]
