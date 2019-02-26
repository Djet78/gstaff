from django.urls import path, include

from .views import (
    ArticleDetail,
    ArticleList,
    ArticleCreateView,
    ArticleChangeView,
    EditorsPublicationsView,
    ArticleDeleteView
)

app_name = 'news'

urlpatterns = [
    path('', ArticleList.as_view(), name='article_list'),
    path('<int:pk>/', ArticleDetail.as_view(), name='article_detail'),
    path('own_publications/', EditorsPublicationsView.as_view(), name='editor_publications'),

    path('article/', include([
        path('add/', ArticleCreateView.as_view(), name='article_create'),
        path('<int:pk>/change', ArticleChangeView.as_view(), name='article_change'),
        path('<int:pk>/delete', ArticleDeleteView.as_view(), name='article_delete'),
    ])),
]
