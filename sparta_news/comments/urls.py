from django.urls import path
from .views import *

urlpatterns = [
    path('<int:article_id>/',CommentView.as_view()),
    path('detail/<int:comment_id>/',CommentDetailView.as_view()),
    path('co/<int:co_comment_id>',CoCommentView.as_view())
]