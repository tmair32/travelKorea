from rest_framework import serializers
from django.contrib.auth import get_user_model

# 유저 전체 정보 조회
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'

# 이메일로 유저 정보 조회
class SearchUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='user_set', many=True, read_only=True)
    class Meta:
        model = get_user_model()
        fields = '__all__'