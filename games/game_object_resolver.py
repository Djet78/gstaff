from games.models import Game, Genre, Platform, Studio
from games.forms import GameForm, GenreForm, PlatformForm, StudioForm

from object_resolver import BaseObjectResolver, ObjectContext


class GameObjectResolver(BaseObjectResolver):
    """ Defines used games app instances for 'ObjectResolver' base class methods """

    URL_INSTANCES_MAPPING = {
        'game': ObjectContext(Game, GameForm, 'name'),
        'genre': ObjectContext(Genre, GenreForm, 'name'),
        'platform': ObjectContext(Platform, PlatformForm, 'name'),
        'studio': ObjectContext(Studio, StudioForm, 'name'),
    }
