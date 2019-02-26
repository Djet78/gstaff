from django.conf import settings
from django.db import models
from django.urls import reverse

from utils import thumbnail
from games.models import Game


class Comment(models.Model):
    article = models.ForeignKey('Article',
                                null=True,
                                blank=True,
                                on_delete=models.CASCADE,
                                related_name='comments')
    game = models.ForeignKey(Game,
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
    ARTICLE = 'a'
    COMMENT = 'c'
    GAME = 'g'

    OBJ_CHOICES = (
        (ARTICLE, 'article'),
        (COMMENT, 'comment'),
        (GAME, 'game'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    obj = models.CharField(max_length=1, choices=OBJ_CHOICES)
    obj_id = models.IntegerField()
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ('-date_added', )

    def __str__(self):
        return f'{self.user} {self.pk}'

    @staticmethod
    def make_complain(user_inst, obj_short_name, obj_pk, body):
        """ Creates and returns complaint obj. If obj was not created returns False. """
        try:
            return Complaint.objects.create(user=user_inst,
                                            obj=obj_short_name,
                                            obj_id=obj_pk,
                                            content=body)
        except ValueError:
            return False


class Article(models.Model):
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.PROTECT,
                              # Restrict choices to admins and editors
                              limit_choices_to=models.Q(is_admin=True) | models.Q(is_editor=True))
    pub_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    image = models.ImageField(upload_to='articles_previews')

    IMAGE_MAX_LENGTH = 300
    IMAGE_MAX_WIDTH = 500

    FILE_FIELDS = ('image', )

    class Meta:
        ordering = ('-pub_date', )

    def __str__(self):
        return f'{self.game} {self.title}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        thumbnail(self.image.path, self.IMAGE_MAX_LENGTH, self.IMAGE_MAX_WIDTH)

    def get_absolute_url(self):
        return reverse('news:article_detail', kwargs={'pk': str(self.pk)})
