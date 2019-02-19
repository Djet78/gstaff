from datetime import date

from django.core.exceptions import ValidationError


def day_is_not_future(value):
    if value > date.today():
        raise ValidationError('Future cannot be set here')
