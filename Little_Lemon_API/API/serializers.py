from rest_framework import serializers
from .models import MenuItem
from django.contrib.auth.models import User,Group

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['title','price','featured','category']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
