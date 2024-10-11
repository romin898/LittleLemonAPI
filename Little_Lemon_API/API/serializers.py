from rest_framework import serializers
from .models import MenuItem,Cart
from django.contrib.auth.models import User,Group

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['title','price','featured','category']

class CartSerializer(serializers.ModelSerializer):
    menuitem = serializers.SlugRelatedField(
        queryset=MenuItem.objects.all(), 
        slug_field='title'
    )    
    class Meta:
        model = Cart
        fields = ['menuitem','quantity','unit_price','price']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
