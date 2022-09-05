from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import User


class RegistrationSerializer(ModelSerializer):
    username = serializers.CharField(max_length=50, required=True)
    name = serializers.CharField(max_length=50, required=True)
    surname = serializers.CharField(max_length=50, required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('name', 'surname', 'password', 'username')

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserLoginSerializer(ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password')


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'surname', 'created_at')
