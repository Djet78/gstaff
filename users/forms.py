from django import forms

from .admin import UserCreationForm
from .models import CustomUser


class UserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('login', 'email', 'nickname', )


class UserChangeProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('nickname', 'avatar', )

# TODO Think how to organize sensitive data updating i.e. pass, login and email
