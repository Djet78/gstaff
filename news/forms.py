from django import forms
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from .models import Complaint, Comment, Article
from gstaff.forms import SearchFormMixin


class CommentAddForm(forms.ModelForm):
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


class ComplaintAddForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ('content', )


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ('owner', )


class SearchNewsForm(SearchFormMixin):
    field_order = ('search', )
