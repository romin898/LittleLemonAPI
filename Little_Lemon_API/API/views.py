from django.shortcuts import render,get_object_or_404
from rest_framework import viewsets, status
from .models import MenuItem
from .serializers import MenuItemSerializer,UserSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.contrib.auth.models import User,Group

# Create your views here.
class MenuItemsView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        GET method to list all menu items
        """
        queryset = MenuItem.objects.all()
        serializer = MenuItemSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        GET method to retrieve a single menu item by ID
        """
        menu_item = get_object_or_404(MenuItem, pk=pk)
        serializer = MenuItemSerializer(menu_item)
        return Response(serializer.data)

    def create(self, request):
        """
        POST method to create a new menu item
        """
        if request.user.groups.filter(name='Manager').exists():
            serializer = MenuItemSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save(user=self.request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'You are not authorized'}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, pk=None):
        """
        PUT method to update an existing menu item
        """
        if request.user.groups.filter(name='Manager').exists():
            menu_item = get_object_or_404(MenuItem, pk=pk)  # Fetch the specific menu item
            serializer = MenuItemSerializer(menu_item, data=request.data)

            if serializer.is_valid():
                serializer.save(user=self.request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'You are not authorized'}, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, pk=None):
        """
        PATCH method to partially update an existing menu item
        """
        if request.user.groups.filter(name='Manager').exists():
            menu_item = get_object_or_404(MenuItem, pk=pk)  # Fetch the specific menu item
            serializer = MenuItemSerializer(menu_item, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save(user=self.request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'You are not authorized'}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        """
        DELETE method to remove a menu item
        """
        if request.user.groups.filter(name='Manager').exists():
            menu_item = get_object_or_404(MenuItem, pk=pk)  # Fetch the specific menu item
            menu_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'You are not authorized'}, status=status.HTTP_403_FORBIDDEN)

class ManagerUsersView(viewsets.ViewSet):
    permission_classes = [IsAdminUser]
    
    def list(self,request):
        """
        GET method to list all Users in Manager Group.
        """
        try:
            manager_group = Group.objects.get(name='Manager')
            manager_users = User.objects.filter(groups=manager_group)
            serializer = UserSerializer(manager_users,many=True)
            return Response(serializer.data,status.HTTP_200_OK)
        
        except Group.DoesNotExist:
            return Response({'error': 'Manager group not found'}, status=status.HTTP_404_NOT_FOUND)

    def create(self,request):
        """
        POST method to create a new manager
        """
        username = request.data['username']
        if username:
            user = get_object_or_404(User,username=username)
            managers = Group.objects.get(name='Manager')
            managers.user_set.add(user)
            return Response({'message':'ok'},status.HTTP_201_CREATED)
        
        return Response({"message":"error"},status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        DELETE method to remove a menu item
        """
        try:
            manager_group = Group.objects.get(name='Manager')
            manager_user = User.objects.filter(groups=manager_group)
            manager_user_n = get_object_or_404(manager_user,pk=pk)
            manager_user_n.delete()
            return Response({'message':'Ok'},status.HTTP_204_NO_CONTENT)
        
        except Group.DoesNotExist:
            return({'message':'Manager Group not Found'},status.HTTP_404_NOT_FOUND)

class DeliveryUsersView(viewsets.ViewSet):
    permission_classes = [IsAdminUser]
    
    def list(self,request):
        """
        GET method to list all Users in Manager Group.
        """
        try:
            delivery_group = Group.objects.get(name='delivery_crew')
            delivery_users = User.objects.filter(groups=delivery_group)
            serializer = UserSerializer(delivery_users,many=True)
            return Response(serializer.data,status.HTTP_200_OK)
        
        except Group.DoesNotExist:
            return Response({'error': 'Delivery Crew group not found'}, status=status.HTTP_404_NOT_FOUND)

    def create(self,request):
        """
        POST method to create a new manager
        """
        username = request.data['username']
        if username:
            user = get_object_or_404(User,username=username)
            delivery_crew = Group.objects.get(name='delivery_crew')
            delivery_crew.user_set.add(user)
            return Response({'message':'ok'},status.HTTP_201_CREATED)
        
        return Response({"message":"error"},status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        DELETE method to remove a menu item
        """
        try:
            delivery_group = Group.objects.get(name='delivery_crew')
            delivery_user = User.objects.filter(groups=delivery_group)
            delivery_user_n = get_object_or_404(delivery_user,pk=pk)
            delivery_user_n.delete()
            return Response({'message':'Ok'},status.HTTP_204_NO_CONTENT)
        
        except Group.DoesNotExist:
            return({'message':'Delivery Group not Found'},status.HTTP_404_NOT_FOUND)
                