from functools import wraps

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404


def user_is_editor(function):
    """ Decorator that can be used to restrict access for everyone, except editors """
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        if request.user.is_editor:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied('This section only available for editors')
    return wrapper


def user_is_owner(model, fk_model_field, unique_model_field, captured_url_group):
    """ Checks is user is object owner

    Assume that we have this model:

        class Car(models.Model):
            owner = models.ForeignKey(UserModel)
            other fields...
    
    This url pattern:

        urlpatterns = [
            path('my_car_num-<int:pk>/', car_detail, name='car_detail'),
        ]

    And our view will be:

        @user_is_owner(Car, 'owner', 'pk', 'pk')
        def car_detail(request, *args, **kwargs):
            ...

    :param model: Model instance
    :param fk_model_field: Relationship field name
    :param unique_model_field: Is used for 'model_obj.objects.get' method lookup
    :param captured_url_group: Url capture group, which value is used for 'model_obj.objects.get' method

    :return: Decorated function if user is model object owner
    """

    def pre_wrap(function):
        @wraps(function)
        def wrapper(request, *args, **kwargs):
            query_params = {unique_model_field: kwargs[captured_url_group]}
            requested_instance = get_object_or_404(model, **query_params)
            actual_owner = getattr(requested_instance, fk_model_field, None)
            if actual_owner == request.user:
                return function(request, *args, **kwargs)
            else:
                raise PermissionDenied('This object doesn\'t belong to you')
        return wrapper
    return pre_wrap
