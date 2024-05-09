from rest_framework import serializers
from .models import *
from datetime import datetime, timedelta
from django.utils.timezone import make_aware, is_aware


class RelativeDateField(serializers.Field):
    def to_representation(self, times):
        now = datetime.now().date()
        times = times.date()
        delta = now - times
        years = delta.days // 365
        days = delta.days
        hours = delta.days * 24
        minutes = delta.seconds // 60

        if years > 0:
            return f"{years} 년전"
        elif days > 0:
            return f"{days} 일전"
        elif hours > 0:
            return f"{hours} 시간전"
        else:
            return f"{minutes} 분전"
        
    


class CoCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Co_Comment
        fields = [
            "content",
        ]
        read_only_fields = ['author']


class CommentViewSerializer(serializers.ModelSerializer):
    co_comments = CoCommentSerializer(many=True, read_only=True)
    date = RelativeDateField(source='created_at')

    class Meta:
        model = Comment
        exclude= (
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
