from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count, F
from .models import Article, ArticleLike
from django.core import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from .serializers import ArticleSerializer

class ArticleListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        articles = Article.objects.all()

        #필터링
        categorie = request.GET.get('categorie')
        if categorie == 'title' :
            search = request.GET.get("search")
            articles = articles.filter(title__contains=search)
        elif categorie == 'content' :
            search = request.GET.get("search")
            articles = articles.filter(content__contains=search)
        elif categorie == 'nickname' :
            search = request.GET.get("search")
            articles = articles.filter(author__contains=search)
        
        #정렬
        order = request.GET.get("order")
        if order == 'comment' :
            articles = articles.annotate(comment_count=Count('comments') + Count('comments__co_comment')).order_by('-comment_count')
        elif order == 'like' :
            pass
        elif order == 'recent' :
            articles = articles.order_by('-created_at')

        #페이지네이션
        paginator = Paginator(articles, 30) 
        page_number = request.GET.get("page")
        if page_number == None:
            serializer = ArticleSerializer(articles, many=True)
        else :
            page_obj = paginator.get_page(page_number)
            serializer = ArticleSerializer(page_obj, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "인증되지 않은 사용자입니다."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    #로그인한 사람만 post
    def dispatch(self, request):
        if request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = []
        return super().dispatch(request)

class ArticleDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Article, pk=pk)

    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, request, pk):
        if not request.user.is_authenticated:
            return Response({"error": "인증되지 않은 사용자입니다."}, status=status.HTTP_401_UNAUTHORIZED)
        article = self.get_object(pk)
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        if not request.user.is_authenticated:
            return Response({"error": "인증되지 않은 사용자입니다."}, status=status.HTTP_401_UNAUTHORIZED)
        article = self.get_object(pk)
        article.delete()
        data = {"pk": f"{pk} is deleted."}
        return Response(data, status=status.HTTP_200_OK)

    
class ArticleLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        article = get_object_or_404(Article, id=pk)
        article_like = ArticleLike.objects.filter(user=request.user,article=article)
        if not article_like.exists():
            like = ArticleLike(user=request.user, article=article)
            like.save()
            return Response("LIKE", status=201)
        else :
            article_like.first().delete()
            return Response("UNLIKE", status=201)