
from django.urls import path, include
from rest_framework import routers

from . import views
from .views import BlogPostView

'''
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'posts', views.BlogPostViewSet)
router.register(r'users', views.UserViewSet)
'''

urlpatterns = [
    path(r'api/', BlogPostView.as_view()),
    path(r'', views.index, name='index')
]