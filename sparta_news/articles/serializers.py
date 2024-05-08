from rest_framework import serializers
from .models import Article
from markdownx.utils import markdown


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        exclude = ('author',)
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        # 작성자 정보를 가져와서 nickname을 data에 추가하는 부분
        author_nickname = instance.author.nickname  # 예시: 작성자의 nickname 필드
        data['author_nickname'] = author_nickname

        data['content'] = markdown(data['content'])
        return data