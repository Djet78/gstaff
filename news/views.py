from django.shortcuts import redirect, render
from django.views.generic import View, DetailView, ListView
from .models import Article
from .forms import CommentForm, ComplaintForm, ArticleForm


class ArticleList(ListView):
    model = Article
    template_name = 'news/article_list.html'
    context_object_name = 'articles'


class ArticleDetail(DetailView):
    model = Article
    template_name = 'news/article_detail.html'
    context_object_name = 'article'


class TestView(View):
    form = ArticleForm
    template = 'news/test.html'

    def get(self, request, *args, **kwargs):
        context = {
            'form': self.form(),
            'res': "It's GET method",
        }
        return render(request, self.template, context)

    def post(self, request, *args, **kwargs):
        if self.form().is_multipart():
            form = self.form(request.POST, request.FILES)
        else:
            form = self.form(request.POST)

        context = {'form': form}
        if form.is_valid():
            obj = form.save()
            return redirect('news:article_detail', pk=obj.pk)

        context['res'] = 'Failure'
        return render(request, self.template, context)
