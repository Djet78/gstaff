from django.views.generic import ListView, DetailView
from .models import Game


class GameList(ListView):
    model = Game
    template_name = 'game_list.html'
    context_object_name = 'games'


class GameDetail(DetailView):
    model = Game
    template_name = 'game_detail.html'
    context_object_name = 'game'
