from rest_framework import serializers
from .models import *
from datetime import datetime, timedelta


class RelativeDateField(serializers.Field):
    def to_representation(self, times):
        now = datetime.now().date()
        times = times.date()
        delta = now - times
        years = delta.days // 365
        days = delta.days
        minutes = delta.seconds // 60

        if years > 0:
            return f"{years} years ago"
        elif days > 0:
            return f"{days} days ago"
        else:
            return f"{minutes} minutes ago"


class CoCommentViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Co_Comment
        fields = [
            "id",
            "content",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # 작성자 정보를 가져와서 nickname을 data에 추가하는 부분
        author_nickname = instance.author.nickname  # 예시: 작성자의 nickname 필드
        data['author_nickname'] = author_nickname
        return data


class CoCommentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Co_Comment
        fields = [
            "content",
        ]
        read_only_fields = ['author']


class CommentViewSerializer(serializers.ModelSerializer):
    co_comments = CoCommentViewSerializer(many=True, read_only=True)
    date = RelativeDateField(source='created_at')

    class Meta:
        model = Comment
        exclude = (
            'author',
            'created_at',
            'article'
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # 작성자 정보를 가져와서 nickname을 data에 추가하는 부분
        author_nickname = instance.author.nickname  # 예시: 작성자의 nickname 필드
        data['author_nickname'] = author_nickname
        return data


class CommentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "content",
        ]
        read_only_fields = ['author']
