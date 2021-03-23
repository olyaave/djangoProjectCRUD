from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import BlogPost
from .serializers import BlogPostSerializer
from .serializers import LoginSerializer
from .serializers import RegistrationSerializer


def index(request, path=''):
    return render(request, 'index.html')


class BlogPostView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        post = BlogPost.objects.all()
        serializer = BlogPostSerializer(post, many=True)
        return Response({"posts": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BlogPostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"message": "Post created successfully"}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        saved_post = get_object_or_404(BlogPost.objects.all(), pk=pk)
        serializer = BlogPostSerializer(instance=saved_post, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({
            "message": "Post {} updated successfully".format(pk)}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        post = get_object_or_404(BlogPost.objects.all(), pk=pk)
        post.delete()
        return Response({
            "message": "Post with id `{}` has been deleted.".format(pk)
        }, status=status.HTTP_200_OK)


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = Response({"message": 'User was created successful.'}, status=status.HTTP_201_CREATED)
        response.set_cookie('Authorization', "Bearer " + serializer.data.get('token', None), max_age=100000, httponly=True, secure=True)
        return response


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = Response({"message": "User was logged in."}, status=status.HTTP_200_OK)
        response.set_cookie('Authorization', "Bearer " + serializer.data.get('token', None), max_age=100000,
                            httponly=True, secure=True)
        return response

    def delete(self, request):
        response = Response({'message': 'User was logged out.'}, status=status.HTTP_200_OK)
        response.delete_cookie('Authorization')
        return response


class AuthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {'username': request.user.username,
             'email': request.user.email
             },
            status=status.HTTP_200_OK)
