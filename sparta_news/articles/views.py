from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from .models import Article
from django.core import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import ArticleSerializer

class ArticleListAPIView(APIView):
    def get(self, request):
        articles = Article.objects.all()
        paginator = Paginator(articles, 30) 
        page_number = request.GET.get("page")
        if page_number == None:
            serializer = ArticleSerializer(articles, many=True)
        else :
            page_obj = paginator.get_page(page_number)
            serializer = ArticleSerializer(page_obj, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class ArticleDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Article, pk=pk)

    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        article = self.get_object(pk)
        article.delete()
        data = {"pk": f"{pk} is deleted."}
        return Response(data, status=status.HTTP_200_OK)
    