from django.conf import settings
from django.db import models
from games.models import Game
from users.models import CustomUser


class Comment(models.Model):
    article = models.ForeignKey('Article',
                                null=True,
                                blank=True,
                                on_delete=models.CASCADE,
                                related_name='comments')
    replies = models.ForeignKey('self',
                                null=True,
                                blank=True,
                                on_delete=models.CASCADE,
                                related_name='comments')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    content = models.TextField()
    votes = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return f'{self.pk}: {self.owner}'


class Complaint(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return f'{self.user} {self.pk}'


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
