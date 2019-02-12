from django.shortcuts import render
from django.views.generic import View, DetailView
from .models import Game, Platform, Studio, Genre
from .forms import SearchGamesForm
from gstaff.forms import SearchBarForm


class GameList(View):
    model = Game
    template_name = 'games/game_list.html'
    search_form = SearchGamesForm

    # Used in dynamic filtering below
    # Keys is form field names, values is django queries
    FIELDS_QUERIES_MAPPING = {
        'platform_name': 'platforms__name__in',
        'studio_name': 'studio__name__in',
        'genre_name': 'genres__name__in',
        'search': 'name__icontains',
        'from_date': 'release_date__year__gte',
        'to_date': 'release_date__year__lte',
    }

    def get(self, request, *args, **kwargs):
        if not request.GET:
            context = {
                'search_form': self.search_form(),
                'games': self.model.objects.all(),
            }
        else:
            search_form = self.search_form(request.GET)
            context = {'search_form': search_form}

            if search_form.is_valid():
                requested = {**search_form.cleaned_data}
                query_params = {self.FIELDS_QUERIES_MAPPING[field]: value for field, value in requested.items() if value}
                context['games'] = self.model.objects.filter(**query_params)

        return render(request, self.template_name, context)


class GameDetail(DetailView):
    model = Game
    template_name = 'games/game_detail.html'
    context_object_name = 'game'


class PlatformList(View):
    model = Platform
    template_name = 'games/platform_list.html'
    search_bar_form = SearchBarForm

    # Used in dynamic filtering below
    # Keys is form field names, values is django queries
    FIELDS_QUERIES_MAPPING = {'search': 'name__icontains'}

    def get(self, request, *args, **kwargs):
        if not request.GET:
            context = {
                'platforms': self.model.objects.all(),
                'search_bar': self.search_bar_form()
            }
        else:
            search_form = self.search_bar_form(request.GET)
            context = {'search_bar': search_form}

            if search_form.is_valid():
                requested = {**search_form.cleaned_data}
                query_params = {self.FIELDS_QUERIES_MAPPING[field]: value for field, value in requested.items() if value}
                context['platforms'] = self.model.objects.filter(**query_params)

        return render(request, self.template_name, context)


class PlatformDetail(DetailView):
    model = Platform
    template_name = 'games/platform_detail.html'
    context_object_name = 'platform'


class StudioList(View):
    model = Studio
    template_name = 'games/studio_list.html'
    search_bar_form = SearchBarForm

    # Used in dynamic filtering below
    # Keys is form field names, values is django queries
    FIELDS_QUERIES_MAPPING = {'search': 'name__icontains'}

    def get(self, request, *args, **kwargs):
        if not request.GET:
            context = {
                'studios': self.model.objects.all(),
                'search_bar': self.search_bar_form()
            }
        else:
            search_form = self.search_bar_form(request.GET)
            context = {'search_bar': search_form}

            if search_form.is_valid():
                requested = {**search_form.cleaned_data}
                query_params = {self.FIELDS_QUERIES_MAPPING[field]: value for field, value in requested.items() if value}
                context['studios'] = self.model.objects.filter(**query_params)

        return render(request, self.template_name, context)


class StudioDetail(DetailView):
    model = Platform
    template_name = 'games/studio_detail.html'
    context_object_name = 'studio'


# ---------------------
class GenreList(View):
    model = Genre
    template_name = 'games/genre_list.html'
    search_bar_form = SearchBarForm

    # Used in dynamic filtering below
    # Keys is form field names, values is django queries
    FIELDS_QUERIES_MAPPING = {'search': 'name__icontains'}

    def get(self, request, *args, **kwargs):
        if not request.GET:
            context = {
                'genres': self.model.objects.all(),
                'search_bar': self.search_bar_form()
            }
        else:
            search_form = self.search_bar_form(request.GET)
            context = {'search_bar': search_form}

            if search_form.is_valid():
                requested = {**search_form.cleaned_data}
                query_params = {self.FIELDS_QUERIES_MAPPING[field]: value for field, value in requested.items() if value}
                context['genres'] = self.model.objects.filter(**query_params)

        return render(request, self.template_name, context)


class GenreDetail(DetailView):
    model = Genre
    template_name = 'games/genre_detail.html'
    context_object_name = 'genre'
