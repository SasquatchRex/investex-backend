from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Share
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Share
        fields = ['id','date','share_symbol', 'share_name', 'quantity', 'buying_price','broker_rate']
