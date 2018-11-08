from django.db import models


class SimpleSTR:

    def __str__(self):
        return self.name


class Studio(SimpleSTR, models.Model):
    name = models.CharField(max_length=50)
    foundation_date = models.DateField()
    description = models.TextField()


class Genre(SimpleSTR, models.Model):
    name = models.CharField(max_length=50)


class Platform(SimpleSTR, models.Model):
    name = models.CharField(max_length=50)


class Game(SimpleSTR, models.Model):
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    studio = models.ForeignKey(Studio, on_delete=models.PROTECT)
    platforms = models.ManyToManyField(Platform)
    description = models.TextField()
    genres = models.ManyToManyField(Genre)
    poster = models.ImageField(upload_to='game_posters')

    class Meta:
        ordering = ['-release_date']
