import jwt
from django.conf import settings
from django.shortcuts import render
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

        response = Response(serializer.data, status=status.HTTP_200_OK)
        response.set_cookie('Authorization', "Bearer " + serializer.data.get('token', None), max_age=1000000)
        return response


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        response.set_cookie('Authorization', "Bearer " + serializer.data.get('token', None), max_age=1000000,
                            httponly=True)
        return response

    def delete(self, request):
        response = Response({'Success'}, status=status.HTTP_200_OK)
        response.delete_cookie('Authorization')
        return response


class UserView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def get(self, request):
        response = Response({"User is not logged in."}, status=status.HTTP_401_UNAUTHORIZED)
        if 'Authorization' in request.COOKIES:
            token_header = request.COOKIES['Authorization']
            token = token_header.split()[1]
            user = self.check_token(token)
            user_bd = get_object_or_404(User.objects.all(), email=user.email)
            if user_bd.password == user.password:
                response = Response({"username": user.username, "email": user.email}, status=status.HTTP_200_OK)
        return response

    def check_token(self, token):

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

        return user
