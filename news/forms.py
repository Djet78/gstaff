from django.forms import ModelForm
from .models import Comment, Complaint, Article


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )


class ComplaintForm(ModelForm):
    class Meta:
        model = Complaint
        fields = ('content', )


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        exclude = ('owner', )
