from django.forms import (
    CheckboxSelectMultiple, RadioSelect,
    ChoiceField,  MultipleChoiceField,
)


class BootstrapMultipleChoiceField(MultipleChoiceField):
    widget = CheckboxSelectMultiple(attrs={'class': 'form-check-input'})


class BootstrapChoiceField(ChoiceField):
    widget = RadioSelect(attrs={'class': 'form-check-input'})
