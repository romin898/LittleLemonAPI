from rest_framework import serializers
from .models import MenuItem,Cart,Order,OrderItem,Category
from django.contrib.auth.models import User,Group

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['slug','title']

class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
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
    delivery_crew = UserSerializer()
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

class OrderPutSerializer(serializers.ModelSerializer):
    class Meta():
        model = Order
        fields = ['delivery_crew','status']

class OrderPutSerializerDelivery(serializers.ModelSerializer):
    class Meta():
        model = Order
        fields = ['status']        