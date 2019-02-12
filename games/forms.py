from django.forms import ModelForm
from .models import Studio, Genre, Platform, Game
from gstaff.forms import SearchFormMixin, YearRangeForm


class StudioCreationForm(ModelForm):
    class Meta:
        model = Studio
        fields = '__all__'


class GenreCreationForm(ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'


class PlatformCreationForm(ModelForm):
    class Meta:
        model = Platform
        fields = '__all__'


class GameCreationForm(ModelForm):
    class Meta:
        model = Game
        fields = '__all__'


class SearchGamesForm(SearchFormMixin, YearRangeForm):
    field_order = ('search', )
