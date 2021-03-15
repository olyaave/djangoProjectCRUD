
from django.urls import path, include, re_path
from rest_framework import routers

from . import views
from .views import BlogPostView, UserView

'''
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'posts', views.BlogPostViewSet)
router.register(r'users', views.UserViewSet)
'''

urlpatterns = [
    re_path(r'api/posts/?', BlogPostView.as_view()),
    path(r'api/posts/<int:pk>', BlogPostView.as_view()),
    path(r'api/check', UserView.as_view()),
    path(r'', views.index, name='index')

]