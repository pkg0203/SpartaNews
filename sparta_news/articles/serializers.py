from rest_framework import serializers
from .models import Article, ArticleLike
from markdownx.utils import markdown
from datetime import datetime, timedelta, timezone

class ArticleSerializer(serializers.ModelSerializer):
    created_string = serializers.SerializerMethodField()

    class Meta:
        model = Article
        exclude = ('author',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # 작성자 정보를 가져와서 nickname을 data에 추가하는 부분
        author_nickname = instance.author.nickname  # 예시: 작성자의 nickname 필드
        data['author_nickname'] = author_nickname
        data['content'] = markdown(data['content'])
        data['like_count'] = ArticleLike.objects.filter(article_id=instance.id).count()
        return data

    def get_created_string(self, instance):
        time_diff = datetime.now(timezone.utc) - instance.created_at
        if time_diff < timedelta(minutes=1):
            return '방금 전'
        elif time_diff < timedelta(hours=1):
            return str(int(time_diff.seconds / 60)) + '분 전'
        elif time_diff < timedelta(days=1):
            return str(int(time_diff.seconds / 3600)) + '시간 전'
        elif time_diff < timedelta(days=7):
            days_diff = datetime.now(timezone.utc).date() - instance.created_at.date()
            return str(days_diff.days) + '일 전'
        else:
            return instance.created_at.strftime("%Y-%m-%d %H:%M:%S")