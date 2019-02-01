from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomUserManager(BaseUserManager):

    def _create_user(self, login, email, password, nickname, **extra_fields):
        if not login or not email:
            raise ValueError('Users must provide login and email')

        user = self.model(
            email=self.normalize_email(email),
            login=login,
            nickname=nickname,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, login, email,  password, nickname='Guest', **extra_fields):
        return self._create_user(login, email, password, nickname, **extra_fields)

    def create_superuser(self, login, email, password, nickname='Admin', **extra_fields):
        return self._create_user(login, email, password, nickname, is_admin=True, **extra_fields)


class CustomUser(AbstractBaseUser):
    login = models.CharField(max_length=50, unique=True)
    nickname = models.CharField(max_length=40, blank=True, default='User')
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='users_avatars', null=True, blank=True)
    date_joined = models.DateField(auto_now_add=True, editable=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_editor = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email', ]

    class Meta:
        ordering = ['-date_joined']

    # TODO finish implementations of methods below
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin or self.is_editor

    def __str__(self):
        return self.login
