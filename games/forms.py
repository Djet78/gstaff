from django.forms import ModelForm
from .models import Studio, Genre, Platform, Game


class StudioForm(ModelForm):
    class Meta:
        model = Studio
        fields = '__all__'


class GenreForm(ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'


class PlatformForm(ModelForm):
    class Meta:
        model = Platform
        fields = '__all__'


class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = '__all__'


