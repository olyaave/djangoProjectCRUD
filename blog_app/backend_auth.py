from urllib.parse import unquote

import jwt

from django.conf import settings
from rest_framework import authentication, exceptions, HTTP_HEADER_ENCODING
from rest_framework.utils import json

from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Bearer'

    def authenticate(self, request):

        request.user = None
        cookie = request.META.get('HTTP_COOKIE')

        if not cookie:
            return None

        try:
            auth_header = cookie.replace('"', '').split('=')[1]
            auth_header = str(auth_header).split()
            auth_header_prefix = self.authentication_header_prefix.lower()

            prefix = auth_header[0]
            token = auth_header[1]

        except:
            msg = 'Invalid authentication. No Token specified.'
            raise exceptions.AuthenticationFailed(msg)

        if prefix.lower() != auth_header_prefix:
            msg = 'Invalid authentication. No Token specified.'
            raise exceptions.AuthenticationFailed(msg)

        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except:
            msg = 'Invalid authentication. Could not decode token.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            msg = 'No user matching this token was found.'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = 'This user has been deactivated.'
            raise exceptions.AuthenticationFailed(msg)

        return user, token
