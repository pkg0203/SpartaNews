from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from articles.models import Article
from .serializers import *


class CommentView(APIView):
    def get(self, request, article_id):
        comment = Comment.objects.filter(article=article_id)
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data)

    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        comment.delete()
        return Response({f'pk : {comment_id} had successfully been deleted.'})
