from django.db import models
from django.conf import settings
from markdownx.models import MarkdownxField

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=120)
    content = MarkdownxField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    url = models.URLField()
    