
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from blogApp.views import RegistrationAPIView, LoginAPIView

urlpatterns = [
    re_path(r'^admin/?', admin.site.urls),
    re_path(r'^', include('blogApp.urls')),
    re_path(r'^registration/?$', RegistrationAPIView.as_view(), name='user_registration'),
    re_path(r'^login/?$', LoginAPIView.as_view(), name='user_login'),
]


