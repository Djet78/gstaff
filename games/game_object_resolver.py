from games.models import Game, Genre, Platform, Publisher, Studio
from games.forms import GameForm, GenreForm, PlatformForm, PublisherForm, StudioForm
from utils.object_resolver import BaseObjectResolver, ObjectContext


class GameObjectResolver(BaseObjectResolver):
    """ Defines games app instances for 'BaseObjectResolver' methods """

    URL_INSTANCE_MAPPING = {
        'game': ObjectContext(Game, GameForm, 'name'),
        'genre': ObjectContext(Genre, GenreForm, 'name'),
        'platform': ObjectContext(Platform, PlatformForm, 'name'),
        'publisher': ObjectContext(Publisher, PublisherForm, 'name'),
        'studio': ObjectContext(Studio, StudioForm, 'name'),
    }
