from rest_framework import serializers
from .models import Post, PostImage
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number']


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['id', 'post', 'image']


class PostSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, required=False)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author',
                  'images', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']
