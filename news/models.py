from django.conf import settings
from django.db import models
from django.urls import reverse

from games.models import Game
from users.models import CustomUser


class Comment(models.Model):
    # TODO Tie this model to other instances (Comment, Article, Game?)
    # Maybe create list of choices for all related instances for 'object' attr
    article = models.ForeignKey('Article',
                                null=True,
                                blank=True,
                                on_delete=models.CASCADE,
                                related_name='comments')
    reply_to = models.ForeignKey('self',
                                 null=True,
                                 blank=True,
                                 on_delete=models.CASCADE,
                                 related_name='replies')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    content = models.TextField()
    votes = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ('date_added', )

    def __str__(self):
        return f'{self.pk}: {self.owner}'


class Complaint(models.Model):
    # TODO Tie this model to other instances (Comment, Article, User?)
    # Maybe create list of choices for all related instances for 'object' attr
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ('-date_added', )

    def __str__(self):
        return f'{self.user} {self.pk}'


class Article(models.Model):
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    pub_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    image = models.ImageField(upload_to='articles_previews')

    class Meta:
        ordering = ('-pub_date', )

    def __str__(self):
        return f'{self.game} {self.title}'

    def get_absolute_url(self):
        return reverse('news:article_detail', kwargs={'pk': str(self.pk)})
