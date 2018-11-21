from django.db import models
from gstaff.validators import day_is_not_future


class SimpleOrderingAndSTR:

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Studio(SimpleOrderingAndSTR, models.Model):
    name = models.CharField(max_length=50)
    foundation_date = models.DateField(validators=[day_is_not_future])
    description = models.TextField()


class Genre(SimpleOrderingAndSTR, models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)


class Platform(SimpleOrderingAndSTR, models.Model):
    name = models.CharField(max_length=50)


class Game(SimpleOrderingAndSTR, models.Model):
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    studio = models.ForeignKey(Studio, on_delete=models.PROTECT)
    platforms = models.ManyToManyField(Platform)
    description = models.TextField()
    genres = models.ManyToManyField(Genre)
    poster = models.ImageField(upload_to='game_posters')

    class Meta:
        ordering = ['-release_date']
