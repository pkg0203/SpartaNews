from rest_framework import serializers
from .models import User
from rest_framework.serializers import Serializer
from drf_recaptcha.fields import ReCaptchaV3Field


class V3Serializer(Serializer):
    recaptcha = ReCaptchaV3Field(action="example")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'nickname', 'password']

        extra_kwargs = {
            'password': {'write_only': True}
        }

    #비밀번호 유효성 검사
    def validate_password(self, value):
        if len(value) < 5:
            raise serializers.ValidationError()
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError()
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError()
        return value
    
    #비밀번호 암호화
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname']
        read_only_fields = ['username']
