from django.db import models
from gstaff.validators import day_is_not_future


class Studio(models.Model):
    name = models.CharField(unique=True, max_length=50)
    foundation_date = models.DateField(validators=[day_is_not_future])
    description = models.TextField(default='No description.')

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(unique=True, max_length=50)
    description = models.TextField(default='No description.')

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class Platform(models.Model):
    name = models.CharField(unique=True, max_length=50)
    description = models.TextField(default='No description.')

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(unique=True, max_length=100)
    release_date = models.DateField()
    studio = models.ForeignKey(Studio, on_delete=models.PROTECT)
    platforms = models.ManyToManyField(Platform, related_name='games')
    description = models.TextField()
    genres = models.ManyToManyField(Genre, related_name='games')
    poster = models.ImageField(upload_to='game_posters')

    class Meta:
        ordering = ('-release_date', )

    def __str__(self):
        return self.name
