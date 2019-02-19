from django import forms


class SearchBarForm(forms.Form):
    search = forms.CharField(max_length=100, required=False)
