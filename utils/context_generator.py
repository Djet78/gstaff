class ContextGenerator:
    """ Implements 'get_context' method, which returns template context. Includes form and filtered queryset

    Used overwritten subclass variables to filter objects queryset:
        model = Django Model instance
        search_form = Django Form instance
        FIELDS_QUERIES_MAPPING = dictionary of a kind: {'form_field_name': 'django_query'}.
            For example:
                FIELDS_QUERIES_MAPPING = {
                    'platform_name': 'platforms__name__in',
                    'studio_name': 'studio__name__in',
                    etc.,
                }
    """

    FIELDS_QUERIES_MAPPING = dict()

    model = None
    search_form = None

    # TODO May be split this on smaller funcs
    # TODO Change returned value to tuple (form, queryset)
    def get_form_queryset_context(self, requested, form_context_name, queryset_context_name):
        """ Return context dictionary with form and queryset

        Filter queryset depending on given 'requested' dict.
        If requested is empty - returns 'model.objects.all()' as queryset context

        :param requested: request.GET or request.POST dict
        :param form_context_name: this value will be set to a form context name
        :param queryset_context_name: this value will be set to a queryset context name

        :return: {form_name: self.search_form, obj_context_name: filtered_queryset}
        """
        if not requested:
            context = {
                form_context_name: self.search_form(),
                queryset_context_name: self.model.objects.all(),
            }
        else:
            search_form = self.search_form(requested)
            context = {form_context_name: search_form}

            if search_form.is_valid():
                requested = {**search_form.cleaned_data}
                query_params = {
                    self.FIELDS_QUERIES_MAPPING[field]: value for field, value in requested.items() if value
                }
                context[queryset_context_name] = self.model.objects.filter(**query_params)
        return context
