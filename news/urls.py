from django.urls import path
from .views import ArticleDetail, ArticleList

app_name = 'news'

urlpatterns = [
    path('', ArticleList.as_view(), name='article_list'),
    path('<int:pk>/', ArticleDetail.as_view(), name='article_detail'),
]
