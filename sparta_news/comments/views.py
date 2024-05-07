from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from articles.models import Article
from .serializers import *


class CommentView(APIView):
    def get(self, request, article_id):
        comment = Comment.objects.filter(article=article_id)
        serializer = CommentViewSerializer(comment, many=True)
        return Response(serializer.data)

    def post(self, request, article_id):
        serializer = CommentWriteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user,
                            article=get_object_or_404(Article, article_id))
            return Response(serializer.data, status=HTTP_201_CREATED)
        
    def put(self, request, comment_id):
        comment = get_object_or_404(Comment,pk = comment_id)
        serializer = CommentWriteSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        comment.delete()
        return Response({f'pk : {comment_id} had successfully been deleted.'})
