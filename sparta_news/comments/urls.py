from django.urls import path
from .views import *

urlpatterns = [
    path('<int:id>/',CommentView.as_view()),
    path('co/<int:id>',CoCommentView.as_view())
]