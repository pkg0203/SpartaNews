from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import *
from articles.models import Article
from .serializers import *


class CommentView(APIView):
    permission_classes = [IsAuthenticated]

    # 대댓글까지 get하는 것은 아직 구현하지 않음
    def get(self, request, article_id):
        comment = Comment.objects.filter(article=article_id)
        serializer = CommentViewSerializer(comment, many=True)
        print(serializer)
        return Response(serializer.data)

    def post(self, request, article_id):
        serializer = CommentWriteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user, article=get_object_or_404(Article, pk=article_id))
            return Response(serializer.data, status=HTTP_201_CREATED)
        
    #로그인한 사람만 post
    def dispatch(self, request, article_id):
        if request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = []
        return super().dispatch(request, article_id)


class CommentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        serializer = CoCommentWriteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user,
                            comment_at=get_object_or_404(Comment, pk=comment_id))
            return Response(serializer.data, status=HTTP_201_CREATED)

    def put(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        if request.user == comment.author:
            serializer = CommentWriteSerializer(
                comment, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        else:
            return Response({"본인 댓글만 수정할 수 있습니다."})

    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        if request.user == comment.author:
            comment.delete()
            return Response({f'pk : {comment_id} had successfully been deleted.'})
        return Response({"본인 댓글만 삭제할 수 있습니다."})



class CoCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, co_comment_id):
        co_comment = get_object_or_404(Co_Comment, pk=co_comment_id)
        if request.user == co_comment.author:
            serializer = CoCommentWriteSerializer(
                co_comment, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        return Response({"본인 대댓글만 수정할 수 있습니다."})

    def delete(self, request, co_comment_id):
        co_comment = get_object_or_404(Co_Comment, pk=co_comment_id)
        if request.user == co_comment.author:
            co_comment.delete()
            return Response({f'pk : {co_comment_id} had successfully been deleted.'})
        return Response({"본인 대댓글만 삭제할 수 있습니다."})