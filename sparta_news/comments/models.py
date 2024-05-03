from django.db import models
from django.conf import settings

# Create your models here.


class Comment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Co_Comment(Comment):
    comment_at = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE
    )