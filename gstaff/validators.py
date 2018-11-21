from django.core.exceptions import ValidationError
from datetime import date


def day_is_not_future(value):
    if value > date.today():
        raise ValidationError('Future cannot be set here')
