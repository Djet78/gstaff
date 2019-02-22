from django.db import models
from django.urls import reverse

from utils import thumbnail
from utils.validators import day_is_not_future


class NaturalKeyManager(models.Manager):
    """ Implements only 'get_by_natural_key' method using 'name' model field name

    I use it since all games models can be referenced by 'name' model field
    and don't have other specific features
    """
    def get_by_natural_key(self, name):
        return self.get(name=name)


class Studio(models.Model):
    objects = NaturalKeyManager()

    name = models.CharField(unique=True, max_length=50)
    logo = models.ImageField(upload_to='studio_logos')
    foundation_date = models.DateField(validators=[day_is_not_future])
    description = models.TextField(default='No description.')

    LOGO_MAX_HEIGHT = 300
    LOGO_MAX_WIDTH = 300

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        thumbnail(self.logo.path, self.LOGO_MAX_HEIGHT, self.LOGO_MAX_WIDTH)

    def get_absolute_url(self):
        return reverse('games:studio_detail', kwargs={'name': self.name})

    def natural_key(self):
        return (self.name, )


class Genre(models.Model):
    objects = NaturalKeyManager()

    name = models.CharField(unique=True, max_length=50)
    description = models.TextField(default='No description.')

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('games:genre_detail', kwargs={'name': self.name})

    def natural_key(self):
        return (self.name, )


class Platform(models.Model):
    objects = NaturalKeyManager()

    name = models.CharField(unique=True, max_length=50)
    photo = models.ImageField(upload_to='platform_photos')
    description = models.TextField(default='No description.')

    PHOTO_MAX_LENGTH = 300
    PHOTO_MAX_WIDTH = 300

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        thumbnail(self.photo.path, self.PHOTO_MAX_LENGTH, self.PHOTO_MAX_WIDTH)

    def get_absolute_url(self):
        return reverse('games:platform_detail', kwargs={'name': self.name})

    def natural_key(self):
        return (self.name, )


class Game(models.Model):
    objects = NaturalKeyManager()

    name = models.CharField(unique=True, max_length=100)
    release_date = models.DateField()
    studio = models.ForeignKey(Studio, on_delete=models.PROTECT)
    platforms = models.ManyToManyField(Platform, related_name='games')
    description = models.TextField()
    genres = models.ManyToManyField(Genre, related_name='games')
    poster = models.ImageField(upload_to='game_posters')

    POSTER_MAX_LENGTH = 400
    POSTER_MAX_WIDTH = 600

    class Meta:
        ordering = ('-release_date', )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        thumbnail(self.poster.path, self.POSTER_MAX_LENGTH, self.POSTER_MAX_WIDTH)

    def get_absolute_url(self):
        return reverse('games:game_detail', kwargs={'name': self.name})

    def natural_key(self):
        return (self.name, )
