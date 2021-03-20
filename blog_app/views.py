import time
from datetime import datetime

import jwt
from django.conf import settings
from django.shortcuts import render
from django.utils.timezone import now
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions

from .models import User
from .models import BlogPost
from .serializers import BlogPostSerializer
from .serializers import LoginSerializer
from .serializers import AuthSerializer
from .serializers import RegistrationSerializer


def index(request, path=''):
    return render(request, 'index.html')


class BlogPostView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        post = BlogPost.objects.all()
        serializer = BlogPostSerializer(post, many=True)
        return Response({"posts": serializer.data})

    def post(self, request):
        serializer = BlogPostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"success": "Post created successfully"})

    def put(self, request, pk):
        saved_post = get_object_or_404(BlogPost.objects.all(), pk=pk)
        serializer = BlogPostSerializer(instance=saved_post, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({
            "success": "Post {} updated successfully".format(pk)
        })

    def delete(self, request, pk):
        post = get_object_or_404(BlogPost.objects.all(), pk=pk)
        post.delete()
        return Response({
            "message": "Post with id `{}` has been deleted.".format(pk)
        }, status=204)


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = Response('User was created successful.', status=status.HTTP_200_OK)
        response.set_cookie('Authorization', "Bearer " + serializer.data.get('token', None), max_age=100000)
        return response


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = Response({"info": "User was logged in."},  status=status.HTTP_200_OK)
        response.set_cookie('Authorization', "Bearer " + serializer.data.get('token', None), max_age=100000,
                            httponly=True)
        return response

    def delete(self, request):
        response = Response({'info': 'Success'}, status=status.HTTP_200_OK)
        response.delete_cookie('Authorization')
        return response


class UserView(APIView):
    permission_classes = [AllowAny]
    serializer_class = AuthSerializer

    def get(self, request):
        token = str(request.COOKIES['Authorization']).split()[1]
        serializer = self.serializer_class(data={'token': token})
        serializer.is_valid(raise_exception=True)
        return Response(
            {'info': "User is logged in.",
             'username': serializer.data.get('username'),
             'email': serializer.data.get('email')},
            status=status.HTTP_200_OK)
