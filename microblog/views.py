from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

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
        response.set_cookie('Authorization', "Bearer " + serializer.data.get('token', None))
        return response


class LoginAPIView(APIView):
    """
    Logs in an existing user.
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        """
        Checks is user exists.
        Email and password are required.
        Returns a JSON web token.
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        response.set_cookie('Authorization', "Bearer " + serializer.data.get('token', None))
        return response


'''
class UserViewSet(viewsets.ModelViewSet):
    """
    Provides basic CRUD functions for the User model
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class BlogPostViewSet(viewsets.ModelViewSet):
    """
    Provides basic CRUD functions for the Blog Post model
    """
    queryset = BlogPost.objects.all()
    serializer_class = serializers.BlogPostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
'''
