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
        fields = "__all__"


class CommentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "content",
        ]
        read_only_fields = ['author']
