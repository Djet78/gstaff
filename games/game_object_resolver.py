from games.models import Game, Genre, Platform, Studio
from games.forms import GameForm, GenreForm, PlatformForm, StudioForm

from object_resolver import BaseObjectResolver, ObjectContext


class GameObjectResolver(BaseObjectResolver):
    """ Defines games app instances for 'BaseObjectResolver' methods """

    URL_INSTANCE_MAPPING = {
        'games': ObjectContext(Game, GameForm, 'name'),
        'genres': ObjectContext(Genre, GenreForm, 'name'),
        'platforms': ObjectContext(Platform, PlatformForm, 'name'),
        'studios': ObjectContext(Studio, StudioForm, 'name'),
    }
