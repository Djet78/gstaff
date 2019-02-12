from django import forms
from games.models import Genre, Platform, Studio


class SearchBarForm(forms.Form):
    search = forms.CharField(max_length=100, required=False)


class PlatformMulCheckForm(forms.Form):
    platform_name = forms.MultipleChoiceField(
        choices=lambda: [(obj['name'], obj['name']) for obj in Platform.objects.values('name')],
        required=False,
        widget=forms.CheckboxSelectMultiple
    )


class StudioMulCheckForm(forms.Form):
    studio_name = forms.MultipleChoiceField(
        choices=lambda: [(obj['name'], obj['name']) for obj in Studio.objects.values('name')],
        required=False,
        widget=forms.CheckboxSelectMultiple
    )


class GenreMulCheckForm(forms.Form):
    genre_name = forms.MultipleChoiceField(
        choices=lambda: [(obj['name'], obj['name']) for obj in Genre.objects.values('name')],
        required=False,
        widget=forms.CheckboxSelectMultiple
    )


class SearchFormMixin(SearchBarForm, PlatformMulCheckForm, StudioMulCheckForm, GenreMulCheckForm):
    pass
