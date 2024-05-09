from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework import status
from .serializers import *
from django.shortcuts import get_object_or_404
from accounts.models import User
from django.http import JsonResponse
from django.conf import settings
from django.views.generic import View
from rest_framework.permissions import IsAuthenticated
import requests
from drf_recaptcha.fields import ReCaptchaV3Field
# Create your views here.


class User(APIView):
    # create user
    def post(self, request):
        # recaptcha_token = request.POST.get('recaptcha_token')

        # recaptcha_response = requests.post(
        #     'https://www.google.com/recaptcha/api/siteverify',
        #     data={
        #         'secret': settings.DRF_RECAPTCHA_SECRET_KEY,
        #         'response': recaptcha_token
        #     }
        # )

        # recaptcha_data = recaptcha_response.json()
        # if recaptcha_data['success']:
        #     serializer = UserSerializer(data=request.data)
        #     if serializer.is_valid(raise_exception=True):
        #         serializer.save()
        #         return Response(serializer.data, status=status.HTTP_201_CREATED)
        #     else:
        #         return JsonResponse({'error': '인증이 실패하였습니다.'})
        # else:
        #     return JsonResponse({'error': 'reCAPTCHA 검증에 실패했습니다.'})
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, id):
        user = get_object_or_404(get_user_model(), id=id)
        return user
    # read user info
    def get(self, request, id):
        user = self.get_object(id)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)

    # modify user info
    def put(self, request, id):
        if request.user.id != int(id):
            return Response({"error": "인증되지 않은 사용자입니다."}, status=status.HTTP_403_FORBIDDEN)
        user = self.get_object(id)
        serializer = UserDetailSerializer(user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    # delete user
    def delete(self, request, id):
        if request.user.id != int(id):
            return Response({"error": "인증되지 않은 사용자입니다."}, status=status.HTTP_403_FORBIDDEN)
        user = self.get_object(id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
