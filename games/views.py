from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.views.generic import View, DetailView
from django.utils.decorators import method_decorator

from .models import Game, Platform, Studio, Genre
from .forms import SearchGamesForm
from .game_object_resolver import GameObjectResolver
from object_resolver.exceptions import BadRequestError, NotFoundError
from gstaff.forms import SearchBarForm
from users.decorators import user_is_editor


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#               Data Displaying Views
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

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
    slug_field = 'name'
    slug_url_kwarg = 'name'


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
    slug_field = 'name'
    slug_url_kwarg = 'name'


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
    model = Studio
    template_name = 'games/studio_detail.html'
    context_object_name = 'studio'
    slug_field = 'name'
    slug_url_kwarg = 'name'


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
    slug_field = 'name'
    slug_url_kwarg = 'name'


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#               Data Manipulating Views
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

@method_decorator((login_required, user_is_editor), name='dispatch')
class ObjectCreate(GameObjectResolver, View):
    template_name = 'games/games_object_form.html'
    context = {'submit_btn': 'Create'}

    def get(self, request, instance_name, *args, **kwargs):
        try:
            form = self.get_form(instance_name)
        except BadRequestError:
            return HttpResponseBadRequest()

        self.context['form'] = form()
        return render(request, self.template_name, self.context)

    def post(self, request, instance_name, *args, **kwargs):
        try:
            form = self.get_form(instance_name)
        except BadRequestError:
            return HttpResponseBadRequest()

        form = form(request.POST)
        if form.is_valid():
            obj = form.save()
            return redirect(obj)

        self.context['form'] = form
        return render(request, self.template_name, self.context)


@method_decorator((login_required, user_is_editor), name='dispatch')
class ObjectChange(GameObjectResolver, View):
    template_name = 'games/games_object_form.html'
    context = {'submit_btn': 'Update'}

    def get(self, request, instance_name, slug, *args, **kwargs):
        try:
            instance, form = self.get_obj_form(instance_name, slug)
        except BadRequestError:
            return HttpResponseBadRequest()
        except NotFoundError:
            return HttpResponseNotFound()

        self.context['form'] = form(instance=instance)
        return render(request, self.template_name, self.context)

    def post(self, request, instance_name, slug, *args, **kwargs):
        try:
            instance, form = self.get_obj_form(instance_name, slug)
        except BadRequestError:
            return HttpResponseBadRequest()
        except NotFoundError:
            return HttpResponseNotFound()

        form = form(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            obj = form.save()
            return redirect(obj)

        self.context['form'] = form
        return render(request, self.template_name, self.context)


@method_decorator((login_required, user_is_editor), name='dispatch')
class ObjectDelete(GameObjectResolver, View):
    template_name = 'games/games_object_confirm_delete.html'
    success_template_name = 'games/games_object_success_delete.html'

    def get(self, request, instance_name, slug, *args, **kwargs):
        try:
            context = {'object': self.get_obj(instance_name, slug)}
        except BadRequestError:
            return HttpResponseBadRequest()
        except NotFoundError:
            return HttpResponseNotFound()

        return render(request, self.template_name, context)

    def post(self, request, instance_name, slug, *args, **kwargs):
        try:
            obj = self.get_obj(instance_name, slug)
        except BadRequestError:
            return HttpResponseBadRequest()
        except NotFoundError:
            return HttpResponseNotFound()

        res, _ = obj.delete()
        if res:
            return render(request, self.success_template_name)

        context = {'object': obj}
        return render(request, self.template_name, context)
