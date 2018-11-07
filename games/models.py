from django.db import models


class Studio(models.Model):
    name = models.CharField(max_length=50)
    foundation_date = models.DateField()
    description = models.TextField()


class Genre(models.Model):
    name = models.CharField(max_length=50)


class Platform(models.Model):
    name = models.CharField(max_length=50)
    release_date = models.DateField()


class Game(models.Model):
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    studio = models.ForeignKey(Studio, on_delete=models.PROTECT)
    # TODO add relation field when articles is created
    platforms = models.ManyToManyField(Platform)
    description = models.TextField()
    genres = models.ManyToManyField(Genre)
    poster = models.ImageField(upload_to='game_posters')
