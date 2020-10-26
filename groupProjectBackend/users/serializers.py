from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    username = serializers.CharField(max_length=200)
    email = serializers.CharField(max_length=200)
    preferred_name = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=100,write_only=True,required=True,style={'input_type': 'password'})

    class Meta:
        model = CustomUser
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