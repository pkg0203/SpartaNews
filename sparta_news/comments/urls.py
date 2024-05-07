from django.urls import path
from .views import *

urlpatterns = [
    path('<int:article_id>/',CommentView.as_view()),
    path('co/<int:id>',CoCommentView.as_view())
]