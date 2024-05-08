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

    def validate_password(self, value):
        if len(value) < 5:
            raise serializers.ValidationError()
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError()
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError()
        return value


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password', 'nickname']
        read_only_fields = ['username']

    def update(self, instance, validated_data):
        if self.context['request'].user.id != instance.id:
            raise serializers.ValidationError()

        instance.password = validated_data.get('password', instance.password)
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.save()
        return instance
