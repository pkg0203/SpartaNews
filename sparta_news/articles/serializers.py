from rest_framework import serializers
from .models import Article
from markdownx.utils import markdown


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['content'] = markdown(data['content'])
        return data