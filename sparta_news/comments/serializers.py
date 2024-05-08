from rest_framework import serializers
from .models import *

class CommentViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

class CommentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "content",
        ]
        read_only='author'

class CoCommentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Co_Comment
        fields = [
            "content",
        ]
        read_only='author'