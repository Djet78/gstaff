from django.forms import CheckboxSelectMultiple, MultipleChoiceField


class BootstrapMultipleChoiceField(MultipleChoiceField):
    widget = CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
