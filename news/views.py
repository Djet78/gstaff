from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from .models import Article, Comment
from .forms import CommentAddForm, SearchNewsForm


class ArticleList(View):
    model = Article
    template_name = 'news/article_list.html'
    search_form = SearchNewsForm

    # Used in dynamic filtering below
    # Keys is form field names, values is django queries
    FIELDS_QUERIES_MAPPING = {
        'platform_name': 'game__platforms__name__in',
        'studio_name': 'game__studio__name__in',
        'genre_name': 'game__genres__name__in',
        'search': 'title__icontains',
    }

    def get(self, request, *args, **kwargs):
        if not request.GET:
            context = {
                'search_form': self.search_form(),
                'articles': self.model.objects.all(),
            }
        else:
            search_form = self.search_form(request.GET)
            context = {'search_form': search_form}

            if search_form.is_valid():
                requested = {**search_form.cleaned_data}
                query_params = {self.FIELDS_QUERIES_MAPPING[field]: value for field, value in requested.items() if value}
                context['articles'] = self.model.objects.filter(**query_params)

        return render(request, self.template_name, context)


class ArticleDetail(View):
    template = 'news/article_detail.html'
    comment_form = CommentAddForm

    def get(self, request, pk, *args, **kwargs):
        context = {
            'article':  get_object_or_404(Article, pk=pk),
            'comment_form': self.comment_form(),
        }
        return render(request, self.template, context)

    # TODO add restriction: user must be authenticated
    def post(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)

        comment_form = self.comment_form(request.POST,
                                         article_obj=article,
                                         # Outer hidden input field value:
                                         parent_comment_id=request.POST.get('parent_comment_id'))

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.owner = request.user

            if request.POST.get('reply_comment'):  # name of submit button
                parent_comment = Comment.objects.get(pk=request.POST.get('parent_comment_id'))
                comment.reply_to = parent_comment
            else:
                comment.article = article

            comment.save()

        context = {
            'article':  article,
            'comment_form': self.comment_form,
        }
        return render(request, self.template, context)
