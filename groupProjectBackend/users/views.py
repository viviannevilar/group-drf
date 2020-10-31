from django.shortcuts import render
from rest_framework.permissions import IsAdminUser,IsAuthenticated 
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserSerializer, CustomUserSerialiser,ChangePasswordSerializer
from rest_framework import permissions, status, generics
from .permissions import OwnProfile
from django.contrib.auth import get_user_model
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
    permission_classes = [IsAdminUser,]
    def get(self, request):
        users = User.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)



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



class ChangePasswordView(generics.UpdateAPIView):
    """An endpoint for changing password."""
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,OwnProfile)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
