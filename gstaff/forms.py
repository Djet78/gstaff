from datetime import date
from django import forms
from django.db.models import Min
from games.models import Game, Genre, Platform, Studio


# TODO remove this to related apps
def get_game_year_choices():
    min_year = Game.objects.aggregate(Min('release_date'))['release_date__min'].year
    curr_year = date.today().year
    return [('', '----')] + [(year, year) for year in range(min_year, curr_year + 1)]


class SearchBarForm(forms.Form):
    search = forms.CharField(max_length=100, required=False)


class PlatformMulChoiceForm(forms.Form):
    platform_name = forms.MultipleChoiceField(
        choices=lambda: ((obj['name'], obj['name']) for obj in Platform.objects.values('name')),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )


class StudioMulChoiceForm(forms.Form):
    studio_name = forms.MultipleChoiceField(
        choices=lambda: ((obj['name'], obj['name']) for obj in Studio.objects.values('name')),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )


class GenreMulChoiceForm(forms.Form):
    genre_name = forms.MultipleChoiceField(
        choices=lambda: ((obj['name'], obj['name']) for obj in Genre.objects.values('name')),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )


class YearRangeForm(forms.Form):
    from_date = forms.ChoiceField(choices=get_game_year_choices,
                                  required=False,
                                  label='From')
    to_date = forms.ChoiceField(choices=get_game_year_choices,
                                required=False,
                                label='To')


class SearchFormMixin(SearchBarForm, PlatformMulChoiceForm, StudioMulChoiceForm, GenreMulChoiceForm):
    pass
