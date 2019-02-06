from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import TestView

app_name = 'users'

urlpatterns = [

    # Test urls
    path('test/', TestView.as_view()),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]
