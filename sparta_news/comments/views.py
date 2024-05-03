from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from articles.models import Article
from .serializers import *

# Create your views here.
class CommentView(APIView):
    def get(self,request,article_id):
        comment=Comment.objects.all()
        serializer = CommentSerializer(comment,many=True)
        return Response(serializer.data)
