from rest_framework import serializers
from .models import *

class CommentViewSerializer(serializers.Serializer):
    class Meta:
        model = Comment
        fields = "__all__"

class CommentWriteSerializer(serializers.Serializer):
    class Meta:
        model = Comment
        fields = [
            "content",
        ]
        read_only='author'

class CoCommentWriteSerializer(serializers.Serializer):
    class Meta:
        model = Co_Comment
        fields = [
            "content",
        ]
        read_only='author'