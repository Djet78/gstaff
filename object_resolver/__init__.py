""" Package aims to reduce the code amount and follows DRY principle, for writing views

Problem:
    Assume have many models (5, for example) in our app which should supply common CRUD operations.
    Django's decision is to create one particular view for every model we have. Follows this way
    we should write 'CreteView' 'UpdateView' and 'DeleteView' for every model we have.

Solution:
    Package defines 'BaseObjectResolver' class with public methods to get desired object related values,
    and process them in one  'CreteView' 'UpdateView' or 'DeleteView' classes.
    See example below with following explanation.

    Assume we have 'games' app.
    I have omit imports for shortness

    # models.py

    # Create our model as usual
    class DevStudio(models.Model):
        name = models.CharField(unique=True, max_length=50)
        description = models.TextField()
        other_fields...


    # forms.py

    # Create form
    class DevStudioForm(ModelForm):
        class Meta:
            model = DevStudio
            fields = '__all__'


    # urls.py

    # register routes
    app_name = 'games'

    urlpatterns = [
        path('<instance_name>/add/', ObjectCreate.as_view(), name='games_object_crete'),
    ]
    # '<instance_name> is key, to search object related instances(Model and Form)


    # game_object_resolver.py

    # Inherit from 'BaseObjectResolver' and overwrite 'URL_INSTANCE_MAPPING'
    class GameObjectResolver(BaseObjectResolver):

        URL_INSTANCE_MAPPING = {
            # <instance_name>: ObjectContext(Model, Form, 'slug_field'),
            'studio': ObjectContext(DevStudio, DevStudioForm, 'name'),
        }
    # 'ObjectContext' is namedtuple instance


    # views.py

    # Write view depending on desired action(CreteView in this case)
    # Notice our 'GameObjectResolver' as paren class
    class ObjectCreate(GameObjectResolver, View):
        template_name = 'games/games_object_form.html'
        context = {'submit_btn': 'Create'}

        def get(self, request, instance_name, *args, **kwargs):
            try:
                form = self.get_form(instance_name) # 'GameObjectResolver' method
            except BadRequestError:                 # 'GameObjectResolver' exception
                return HttpResponseBadRequest()

            self.context['form'] = form()
            return render(request, self.template_name, self.context)

        def post(self, request, instance_name, *args, **kwargs):
            try:
                form = self.get_form(instance_name) # 'GameObjectResolver' method
            except BadRequestError:                 # 'GameObjectResolver' exception
                return HttpResponseBadRequest()

            form = form(request.POST)
            if form.is_valid():
                obj = form.save()
                return redirect(obj)

            self.context['form'] = form
            return render(request, self.template_name, self.context)


    And now if we want to add support for other object we should simply include in in our
    'GameObjectResolver' settings like so:


    # game_object_resolver.py

    class GameObjectResolver(BaseObjectResolver):

        URL_INSTANCE_MAPPING = {
            'studio': ObjectContext(DevStudio, DevStudioForm, 'name'),
            'new_instance': ObjectContext(InstanceModel, InstanceModel, 'pk')
        }


To get more info about methods and Exceptions see source code. Also docs included.
"""

from .base_object_resolver import BaseObjectResolver, ObjectContext
