from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserSerializer, CustomUserSerialiser
from rest_framework import permissions, status
from .permissions import OwnProfile
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.renderers import (
                                        HTMLFormRenderer, 
                                        JSONRenderer, 
                                        BrowsableAPIRenderer,
                                    )

User = get_user_model()

# Create your views here.
class CustomUserList(APIView):
    serializer_class = CustomUserSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, HTMLFormRenderer)
    def get(self, request):
        users = User.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class CustomUserDetail(APIView):
    permission_classes = [permissions.IsAuthenticated,
    OwnProfile]
    
    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise Http404
    def get(self, request, username):
        user = self.get_object(username)
        self.check_object_permissions(request, user)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def put(self, request, username):
        user = self.get_object(username)
        self.check_object_permissions(request, user)
        data = request.data
        serializer = CustomUserSerializer(
            instance=user,
            data=data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    def delete(self, request, username):
        user = self.get_object(username)
        self.check_object_permissions(request, user)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserCreate(generics.CreateAPIView):
    """ url: users/register/ """
    queryset = User.objects.all()
    serializer_class = CustomUserSerialiser