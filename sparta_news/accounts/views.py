from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import *
from django.shortcuts import get_object_or_404
from accounts.models import User

# Create your views here.


class User(APIView):
    # create user
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

    # modify user info
    def put(self, request, id):
        user = get_object_or_404(User, id=id)
        serializer = UserDetailSerializer(user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    # delete user(
    def delete(self, request, id):
        user = get_object_or_404(User, id=id)
        user.delete()
        return Response(status=200)
