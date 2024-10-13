from rest_framework import serializers
from .models import MenuItem,Cart,Order,OrderItem
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

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['delivery_crew','status','total','date']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order','menuitem','quantity']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
