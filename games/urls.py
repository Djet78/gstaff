from django.urls import path
from .views import GameList, GameDetail

app_name = 'games'

urlpatterns = [
    path('', GameList.as_view(), name='game_list'),
    path('<int:pk>', GameDetail.as_view(), name='game_detail'),
]
