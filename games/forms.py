from datetime import date

from django import forms
from django.db.models import Min

from .models import Game, Genre, Platform, Publisher, Studio
from gstaff.forms import SearchBarForm
from gstaff.fields import BootstrapChoiceField, BootstrapMultipleChoiceField


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#               Games Model Forms
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = '__all__'


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'


class PlatformForm(forms.ModelForm):
    class Meta:
        model = Platform
        fields = '__all__'


class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = '__all__'


class StudioForm(forms.ModelForm):
    class Meta:
        model = Studio
        fields = '__all__'


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#               Data Filtering Forms
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

def get_game_year_choices(prepend_empty=True, empty_val=('', '----')):
    """ Creates list years from oldest game in DB, to current year.

    List format is acceptable for forms.ChoiceField.
    Format: [(year_1, year_1), (year_2, year_2), ...]

    :keyword prepend_empty: if set to True (default). List will have empty value at the beginning.
    :keyword empty_val: Value that will be set at the beginning of a list default: ('', '----')

    :return: list of year tuples. Optionally with prepended empty value
    """
    min_year = Game.objects.aggregate(Min('release_date'))['release_date__min'].year
    curr_year = date.today().year
    years = []
    if prepend_empty is True:
        years.append(empty_val)
    years += [(year, year) for year in range(min_year, curr_year + 1)]
    return years


class YearRangeForm(forms.Form):
    from_date = BootstrapChoiceField(choices=get_game_year_choices,
                                     required=False,
                                     label='From')
    to_date = BootstrapChoiceField(choices=get_game_year_choices,
                                   required=False,
                                   label='Until')


class PlatformMulChoiceForm(forms.Form):
    platforms = BootstrapMultipleChoiceField(
        choices=lambda: ((obj['name'], obj['name']) for obj in Platform.objects.values('name')),
        required=False,
    )


class StudioMulChoiceForm(forms.Form):
    studios = BootstrapMultipleChoiceField(
        choices=lambda: ((obj['name'], obj['name']) for obj in Studio.objects.values('name')),
        required=False,
    )


class GenreMulChoiceForm(forms.Form):
    genres = BootstrapMultipleChoiceField(
        choices=lambda: ((obj['name'], obj['name']) for obj in Genre.objects.values('name')),
        required=False,
    )


class GameFiltersMixin(PlatformMulChoiceForm, StudioMulChoiceForm, GenreMulChoiceForm):
    pass


class GamesFilterForm(GameFiltersMixin, YearRangeForm, SearchBarForm):
    field_order = ('search', )
