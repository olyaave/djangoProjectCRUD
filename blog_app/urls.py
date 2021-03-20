
from django.urls import path, re_path

from . import views
from .views import BlogPostView, UserView


urlpatterns = [
    path(r'api/posts/<int:pk>', BlogPostView.as_view()),
    re_path(r'api/posts/?', BlogPostView.as_view()),
    path(r'api/check', UserView.as_view()),
    path(r'', views.index, name='index')
]