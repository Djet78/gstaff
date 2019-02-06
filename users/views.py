from django.shortcuts import redirect, render
from django.views import View
from .forms import UserProfileForm, UserRegisterForm


class TestView(View):
    form = UserProfileForm
    template = 'news/test.html'

    def get(self, request, *args, **kwargs):
        context = {
            'form': self.form(),
            'res': "It's GET method",
        }
        return render(request, self.template, context)

    def post(self, request, *args, **kwargs):
        if self.form().is_multipart():
            form = self.form(request.POST, request.FILES)
        else:
            form = self.form(request.POST)

        context = {'form': form}
        if form.is_valid():
            obj = form.save()
            return redirect('../../admin/users/customuser/')

        context['res'] = 'Failure'
        return render(request, self.template, context)

