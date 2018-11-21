from django.views.generic import ListView, DetailView
from .models import Article


class ArticleList(ListView):
    model = Article
    template_name = 'news/article_list.html'
    context_object_name = 'articles'


class ArticleDetail(DetailView):
    model = Article
    template_name = 'news/article_detail.html'
    context_object_name = 'article'
