from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import View

from .forms import UserChangeProfileForm, UserRegisterForm


class RegisterView(View):
    template_name = 'users/register.html'
    form = UserRegisterForm

    def get(self, request, *args, **kwargs):
        context = {'register_from': self.form()}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        context = {'register_from': self.form}
        if form.is_valid():
            form.save()
            return redirect('users:login')
        return render(request, self.template_name, context)


class ProfileView(LoginRequiredMixin, View):
    template_name = 'users/profile.html'
    profile_form = UserChangeProfileForm

    def get(self, request, *args, **kwargs):
        context = {
            'user': request.user,
            'profile_form': self.profile_form(instance=request.user)
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        profile_form = self.profile_form(request.POST, request.FILES, instance=request.user)
        context = {'user': request.user}
        if profile_form.is_valid():
            profile_form.save()
            context['profile_form'] = profile_form
        return render(request, self.template_name, context)
