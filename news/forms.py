from django import forms
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from .models import Complaint, Comment, Article
from games.models import Genre, Platform, Studio


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )
        labels = {'content': 'Comment'}

    def __init__(self, *args, **kwargs):
        """ Extends Form attributes for further validation """
        self.article = kwargs.pop('article_obj', None)
        self.parent_comment_id = kwargs.pop('parent_comment_id', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        """ Prevents exceptions from misbehaved users, who have changed hidden values from form fields """
        super().clean()
        if self.parent_comment_id:
            exc_msg = 'Dynamic, hidden form values was changed on user side'
            try:
                parent_comment = Comment.objects.get(pk=self.parent_comment_id)
                if parent_comment not in self.article.comments.all():
                    # Raised if user changed comment_id to other comment_id from another article
                    raise ValidationError(exc_msg, code='fake')
            except (ValueError, ObjectDoesNotExist):
                # Raised if user changed comment_id to inappropriate one
                raise ValidationError(exc_msg, code='fake')


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False)


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ('content', )


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ('owner', )


class FilterNewsForm(forms.Form):
    # Django throws exception if you explicitly use this list comprehensions below,
    # before any migrations made.
    # Error: django.db.utils.OperationalError: no such table: 'table_name'
    # But with callables works just fine

    platform_name = forms.MultipleChoiceField(
        choices=lambda: [(obj['name'], obj['name']) for obj in Platform.objects.values('name')],
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    studio_name = forms.MultipleChoiceField(
        choices=lambda: [(obj['name'], obj['name']) for obj in Studio.objects.values('name')],
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    genre_name = forms.MultipleChoiceField(
        choices=lambda: [(obj['name'], obj['name']) for obj in Genre.objects.values('name')],
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
