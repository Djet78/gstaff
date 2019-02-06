from django.urls import path
from .views import GameList, GameDetail, TestView

app_name = 'games'

urlpatterns = [
    path('', GameList.as_view(), name='game_list'),
    path('<int:pk>/', GameDetail.as_view(), name='game_detail'),
    # Test urls
    path('test/', TestView.as_view()),
]
