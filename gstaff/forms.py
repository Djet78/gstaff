from django import forms


class SearchBarForm(forms.Form):
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                'type': 'search',
                'class': 'form-control m-2',
                'placeholder': 'Search',
            }
        )
    )
