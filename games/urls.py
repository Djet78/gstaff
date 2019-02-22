from django.urls import path, include

from .views import (
    GameList, GameDetail,
    GenreList, GenreDetail,
    PlatformList, PlatformDetail,
    StudioList, StudioDetail,
    ObjectCreate, ObjectChange, ObjectDelete
)

app_name = 'games'

urlpatterns = [
    path('games/', include([
        path('', GameList.as_view(), name='game_list'),
        path('<name>/', GameDetail.as_view(), name='game_detail'),
    ])),
    path('platforms/', include([
        path('', PlatformList.as_view(), name='platform_list'),
        path('<name>/', PlatformDetail.as_view(), name='platform_detail'),
    ])),
    path('studios/', include([
        path('', StudioList.as_view(), name='studio_list'),
        path('<name>/', StudioDetail.as_view(), name='studio_detail'),
    ])),
    path('genres/', include([
        path('', GenreList.as_view(), name='genre_list'),
        path('<name>/', GenreDetail.as_view(), name='genre_detail'),
    ])),
    path('<instance_name>/', include([
        path('add/', ObjectCreate.as_view(), name='games_object_crete'),
        path('<slug>/change/', ObjectChange.as_view(), name='games_object_change'),
        path('<slug>/delete/', ObjectDelete.as_view(), name='games_object_delete'),
    ])),
]
