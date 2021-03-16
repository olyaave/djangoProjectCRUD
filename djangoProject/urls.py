
from django.contrib import admin
from django.urls import include, re_path

from blogApp.views import RegistrationAPIView, LoginAPIView

urlpatterns = [
    re_path(r'^admin/?', admin.site.urls),
    re_path(r'^', include('blogApp.urls')),
    re_path(r'^registration/?$', RegistrationAPIView.as_view(), name='user_registration'),
    re_path(r'^login/?$', LoginAPIView.as_view(), name='user_login'),
]


