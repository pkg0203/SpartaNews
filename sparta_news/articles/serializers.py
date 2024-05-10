from rest_framework import serializers
from .models import Article, ArticleLike
from markdownx.utils import markdown
from datetime import datetime, timedelta, timezone
from .ai_test import news_link_ai
from comments.models import Comment

class RelativeDateField(serializers.Field):
    def to_representation(self, times):
        now = datetime.now().date()
        times = times.date()
        delta = now - times
        years = delta.days // 365
        days = delta.days
        hours = delta.seconds // 3600
        minutes = (delta.seconds % 3600) // 60

        if years > 0:
            return f"{years} 년 전"
        elif days > 0:
            return f"{days} 일 전"
        elif hours > 0:
            return f"{hours} 시간 전"
        else:
            return f"{minutes} 분 전"
        
class ArticleSerializer(serializers.ModelSerializer):
    date = RelativeDateField(source='created_at')

    class Meta:
        model = Article
        exclude= (
            'author', 
            'updated_at',
            'created_at',
        )
        extra_kwargs = {
            'content': {'write_only': True},
            'url': {'write_only': True},
        }
        

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # 작성자 정보를 가져와서 nickname을 data에 추가하는 부분
        author_nickname = instance.author.nickname  # 예시: 작성자의 nickname 필드
        data['author_nickname'] = author_nickname
        # data['content'] = markdown(data['content'])
        data['like_count'] = ArticleLike.objects.filter(article_id=instance.id).count()
        return data

class ArticleWriteSerializer(serializers.ModelSerializer) :
    class Meta:
        model = Article
        fields = [
            "title",
            "content",
            "url"
        ]
        read_only_fields = ['author']
        
class ArticleDetailSerializer(ArticleSerializer) :
    class Meta:
        model = Article
        exclude= (
            'author', 
            'updated_at',
            'created_at',
        )
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        news_link = news_link_ai(instance.url)
        data['news_link'] = news_link
        return data
    
