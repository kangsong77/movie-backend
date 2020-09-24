from rest_framework import serializers
from .models import Post

# Booking 모델에 대한 직렬화 클래스 정의


class PostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source='owner.username', read_only=True)

    class Meta:
        model = Post
        fields = ['username', 'movie_title',
                  'movie_rating', 'comment', 'modify_dt']
