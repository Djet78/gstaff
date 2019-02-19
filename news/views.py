from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View, DeleteView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

from context_generator import ContextGenerator
from .models import Article, Comment
from .forms import ArticleForm, CommentAddForm, SearchNewsForm
from users.decorators import user_is_editor, user_is_owner


class ArticleList(ContextGenerator, View):
    model = Article
    template_name = 'news/article_list.html'
    search_form = SearchNewsForm

    FIELDS_QUERIES_MAPPING = {
        'platform_name': 'game__platforms__name__in',
        'studio_name': 'game__studio__name__in',
        'genre_name': 'game__genres__name__in',
        'search': 'title__icontains',
    }

    def get(self, request, *args, **kwargs):

        context = self.get_form_queryset_context(request.GET, 'search_form', 'articles')

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

    @method_decorator(login_required)
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


@method_decorator((login_required, user_is_editor), name='dispatch')
class EditorsPublicationsView(View):
    model = Article
    template_name = 'news/editor_publications.html'

    # TODO may be add some filters for pubs like on main page
    def get(self, request, *args, **kwargs):
        articles = self.model.objects.filter(owner__id=request.user.id)
        context = {'articles': articles}
        return render(request, self.template_name, context)


@method_decorator((login_required, user_is_editor), name='dispatch')
# TODO Use same template for Creation and Changing
class ArticleCreateView(View):
    form = ArticleForm
    template_name = 'news/article_create.html'

    def get(self, request, *args, **kwargs):
        context = {'article_form': self.form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        article_form = self.form(request.POST, request.FILES)

        if article_form.is_valid():
            article = article_form.save(commit=False)
            article.owner = request.user
            article.save()
            return redirect(article)

        context = {'article_form': article_form}
        return render(request, self.template_name, context)


class ArticleChangeView(View):
    model = Article
    form = ArticleForm
    template_name = 'news/article_change.html'
    decoratos = (
        login_required,
        user_is_editor,
        user_is_owner(model, 'owner', 'pk', 'pk'),
    )

    @method_decorator(decoratos)
    def dispatch(self, request, *args, **kwargs):
        article_inst = get_object_or_404(self.model, pk=kwargs['pk'])
        return super().dispatch(request, article_inst, *args, **kwargs)

    def get(self, request, article_inst, *args, **kwargs):
        change_form = self.form(instance=article_inst)
        context = {'article_form': change_form}
        return render(request, self.template_name, context)

    def post(self, request, article_inst, *args, **kwargs):
        change_form = self.form(request.POST, request.FILES, instance=article_inst)

        if change_form.is_valid():
            article = change_form.save()
            return redirect(article)

        context = {'article_form': change_form}
        return render(request, self.template_name, context)


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('news:editor_publications')

    decoratos = (
        login_required,
        user_is_editor,
        user_is_owner(model, 'owner', 'pk', 'pk'),
    )

    @method_decorator(decoratos)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
