
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import get_user_model
from .models import User
from .models import Favorite
from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate
from rest_framework.serializers import ModelSerializer, ReadOnlyField
from rest_framework import serializers

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

User = get_user_model()


class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])

        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)

        if user is None:
            return {
                'email': 'None'
            }
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        return {
            'email': user.email,
            'token': jwt_token
        }

# class UserSerializer(ModelSerializer):
#     class Meta:
#         model = User
#         fields = "__all__"
#         # fields = ["email", "username"]


class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Favorite.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'snippets']


class FavoriteSerializer(serializers.ModelSerializer):
    # user_id = ReadOnlyField(source='owner.username')

    class Meta:
        model = Favorite
        fields = ['tm_id', 'title', 'backdrop_path']
        # fields = ['tm_id', 'title', 'backdrop_path', 'user_id']
