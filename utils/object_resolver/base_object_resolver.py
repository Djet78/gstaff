from collections import namedtuple

from django.core.exceptions import ObjectDoesNotExist

from .exceptions import BadRequestError, NotFoundError


ObjectContext = namedtuple('ObjectContext', 'model, form, slug_field')
ObjectContext.__doc__ += ': Store all data related to app instance'
ObjectContext.model.__doc__ += ': Django model instance'
ObjectContext.form.__doc__ += ': Django Form instance for creating/updating an object'
ObjectContext.slug_field.__doc__ += ': Field name, with unique values, by which you can get the object ' \
                                    'using "model.objects.get()" method'


class BaseObjectResolver:
    """ Resolves with which object view should interact and provides methods to get desired data

    Used to handle many app instances in one particular view class i.e. Create / Update / Delete.
    Defines methods to get object context values, for further processing in views.

    Using child overwritten 'URL_INSTANCE_MAPPING'.
    'URL_INSTANCE_MAPPING' is dict, where keys - values which passes from url i.e.:

        'path('<obj_name>/add/', YourView.as_view(), name='your_view_name')'
        In this example '<obj_name>' is value to compare with 'URL_INSTANCES_MAPPING' keys.

    And values - 'ObjectContext' objects with data related to given <obj_name>.

    'URL_INSTANCE_MAPPING' Example:
        URL_INSTANCE_MAPPING = {
            '<obj_name>: ObjectContext(Model, Form, 'field'),
            'genre': ObjectContext(GenreModel, GenreForm, 'name'),
        }

    See 'ObjectContext' docs to more about fields definition
    """

    URL_INSTANCE_MAPPING = dict()

    def get_form(self, instance_name):
        """ Returns form specified for instance

        :raise 'BadRequestError' if key(instance_name) is not exist

        :param instance_name: should be key from 'URL_INSTANCES_MAPPING'

        :return: Form instance
        """
        obj_context = self._get_instance_context(instance_name)
        return obj_context.form

    def get_obj(self, instance_name, field_val):
        """ Returns object specified for instance

        :raise 'BadRequestError' if key(instance_name) is not exist
        :raise 'NotFoundError' if instance with 'field_val' does not exist

        :param instance_name: should be key from 'URL_INSTANCES_MAPPING'
        :param field_val: value for model.objects.get method

        :return: requested instance object
        """
        obj_context = self._get_instance_context(instance_name)
        model = obj_context.model
        field_name = obj_context.slug_field
        return self._get_obj(model, field_name, field_val)

    def get_obj_form(self, instance_name, field_val):
        """ Same as 'self.get_obj' and 'self.get_form' united

        :return: tuple(object, instance)
        """
        obj_context = self._get_instance_context(instance_name)
        model = obj_context.model
        field_name = obj_context.slug_field
        obj = self._get_obj(model, field_name, field_val)
        return obj, obj_context.form

    def _get_instance_context(self, instance_name):
        """ Returns 'ObjectContext' namedtuple from 'URL_INSTANCES_MAPPING'

        :raise 'BadRequestError' if key(instance_name) is not exist

        :param instance_name: should be key from 'URL_INSTANCES_MAPPING'

        :return: ObjectContext namedtuple
        """
        obj_context = self.URL_INSTANCE_MAPPING.get(instance_name)
        if obj_context is None:
            raise BadRequestError('Not valid instance name was entered in url:{}'.format(instance_name))
        return obj_context

    def _get_obj(self, model, field_name, field_val):
        """ Returns object specified for instance

        :raise 'NotFoundError' if instance with 'field_val' does not exist

        :param model: django Model instance
        :param field_name: unique model field for lookup
        :param field_val: unique field value for lookup

        :return: django Model object instance
        """
        params = {field_name: field_val}
        try:
            obj = model.objects.get(**params)
        except ObjectDoesNotExist:
            raise NotFoundError('Object with this value: "{}" - does not exist'.format(field_val))
        return obj
