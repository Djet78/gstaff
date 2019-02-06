from .admin import UserCreationForm, UserChangeForm
from .models import CustomUser


class UserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('login', 'email', 'nickname', )


class UserProfileForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('login', 'email', 'nickname', 'avatar', )
