from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

# Create your views here.
class User(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        nickname = data.get('nickname')
        password = data.get('password')

        if not id or not nickname:
            return Response(
                {'error': 'username 및 nickname을 모두 입력해주세요.'},
                status=400
            )

        if get_user_model().objects.filter(username=username).exists():
            return Response(
                {'error': '이미 존재하는 username입니다.'},
                status=400
            )

        if get_user_model().objects.filter(nickname=nickname).exists():
            return Response(
                {'error': '이미 존재하는 nickname입니다.'},
                status=400
            )

        user = get_user_model().objects.create_user(
            username=username,
            nickname=nickname,
            password=password,
        )
        return Response(
            {"id": user.id,
            "username": user.username, 
            "nickname": user.nickname, },
            status=201
        )