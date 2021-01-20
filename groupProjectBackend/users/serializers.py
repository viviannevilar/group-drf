from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    username = serializers.CharField(max_length=200)
    email = serializers.CharField(max_length=200)
    preferred_name = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=100,write_only=True,required=True,style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password','preferred_name']

    def create(self, validated_data):
        password = validated_data.pop('password')
        new_user = CustomUser.objects.create(**validated_data)
        new_user.set_password(password)
        new_user.save()
        return new_user

    def update(self, instance, validated_data):
            instance.id = validated_data.get('id', instance.id)
            instance.username = validated_data.get('username', instance.username)
            instance.email = validated_data.get('email', instance.email)
            instance.preferred_name = validated_data.get('preferred_name',instance.preferred_name)
            instance.password = validated_data.get('password', instance.password)
            instance.save()
            return instance


#this is the one being used to create users
class CustomUserSerialiser(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'password','preferred_name')
        lookup_field = 'username'

        # These fields are only editable (not displayed) and have to be a part of 'fields' tuple
        extra_kwargs = {'password': {'write_only': True, 'min_length': 4}}

    def create(self, validated_data):
        user = super(CustomUserSerialiser, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

   
class ChangePasswordSerializer(serializers.Serializer):
    model = User
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


#this is the one being used to create users
class UserShareSerialiser(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username',]
