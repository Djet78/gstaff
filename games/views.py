from django.shortcuts import render, redirect
from django.views.generic import View, DetailView, ListView
from .models import Game
from .forms import StudioForm, GenreForm, PlatformForm, GameForm


class GameList(ListView):
    model = Game
    template_name = 'games/game_list.html'
    context_object_name = 'games'


class GameDetail(DetailView):
    model = Game
    template_name = 'games/game_detail.html'
    context_object_name = 'game'


class TestView(View):
    form = GameForm
    template = 'news/test.html'

    def get(self, request, *args, **kwargs):
        context = {
            'form': self.form(),
            'res': "It's GET method",
        }
        return render(request, self.template, context)

    def post(self, request, *args, **kwargs):
        if self.form().is_multipart():
            form = self.form(request.POST, request.FILES)
        else:
            form = self.form(request.POST)

        context = {'form': form}
        if form.is_valid():
            obj = form.save()
            return redirect('games:game_detail', pk=obj.pk)

        context['res'] = 'Failure'
        return render(request, self.template, context)
