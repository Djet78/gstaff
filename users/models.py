from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from utils import thumbnail


class CustomUserManager(BaseUserManager):

    def _create_user(self, login, email, password, nickname, **extra_fields):
        if not login or not email:
            raise ValueError('Users must provide login and email.')

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
    nickname = models.CharField(max_length=40,
                                blank=True,
                                default='User',
                                help_text="Used as your name on site. That's not unique.")
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='users_avatars', null=True, blank=True)
    date_joined = models.DateField(auto_now_add=True, editable=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_editor = models.BooleanField(default=False)
    _warnings = models.IntegerField(default=0, verbose_name='warnings')

    objects = CustomUserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ('email', )

    AVATAR_MAX_HEIGHT = 300
    AVATAR_MAX_WIDTH = 300

    FILE_FIELDS = ('avatar', )

    # If user exceed this amount, user will be banned.
    MAX_WARNINGS = 5

    class Meta:
        ordering = ('-date_joined', )

    def __str__(self):
        return self.nickname

    def save(self, *args, **kwargs):
        if self.avatar:
            thumbnail(self.avatar.path, self.AVATAR_MAX_HEIGHT, self.AVATAR_MAX_WIDTH)
        if self._warnings >= self.MAX_WARNINGS:
            self.ban()
        super().save(*args, **kwargs)

    # 'has_perm' and 'has_module_perms' used for Django admin page access only.
    # You'll no longer be able to get there if you remove them.
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def warnings(self):
        return self._warnings

    def add_warning(self):
        self._warnings += 1

    def reset_warnings(self):
        self._warnings = 0

    def ban(self):
        """ Sets 'is_active" to: False. """
        self.is_active = False

    def unban(self):
        """ Sets '_warnings' to: 0 , and  'is_active" to: True. """
        self.reset_warnings()
        self.is_active = True
