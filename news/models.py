from django.conf import settings
from django.db import models
from games.models import Game


class Comment(models.Model):
    # TODO figure out how to implement relations with itself (May be try recursion in view and extract context?)
    # May be Articles should refer to comments and comments should refer to themselves
    # And afterwards i may use {% as? cycle silent %}??
    # forloop.parentloop ??
    article = models.ForeignKey('Article',
                                null=True,
                                blank=True,
                                on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    content = models.TextField()
    votes = models.IntegerField(default=0)
    replies = models.ForeignKey('self',
                                null=True,
                                blank=True,
                                on_delete=models.CASCADE)
    add_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk}: {self.owner}'


class Article(models.Model):
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    pub_date = models.DateField(auto_now_add=True)
    content = models.TextField()
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    image = models.ImageField(upload_to='articles_previews')

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return f'{self.game} {self.title}'
