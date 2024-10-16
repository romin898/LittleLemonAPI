from django.shortcuts import render,get_object_or_404
from rest_framework import viewsets, status
from .models import MenuItem,Cart,Order,OrderItem
from .serializers import MenuItemSerializer,UserSerializer, CartSerializer,OrderPutSerializer,OrderItemSerializer,OrderSerializer,\
OrderPutSerializerDelivery
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.contrib.auth.models import User,Group
from decimal import Decimal
from datetime import date
from django.core.paginator import Paginator, EmptyPage
from rest_framework.throttling import AnonRateThrottle,UserRateThrottle

# Create your views here.
class MenuItemsView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    throtling_classes = [UserRateThrottle]
    def list(self, request):
        """
        GET method to list all menu items
        """
        queryset = MenuItem.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        price = request.query_params.get('price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage',default=2)
        page = request.query_params.get('page',default=1)
        if category_name:
            queryset = queryset.filter(category__title__iexact=category_name)
        if price:
            queryset = queryset.filter(price__lte=price)
        if search:
            queryset = queryset.filter(title__icontains=search)
        if ordering:
            ordering_fields = ordering.split(',')
            queryset = queryset.order_by(*ordering_fields)
        paginator = Paginator(queryset,per_page=perpage)
        try:
            queryset = paginator.page(number=page)
        except EmptyPage:
            queryset=[]    

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

class CartManagementView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        GET method to list all the items in cart
        """
        queryset = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        POST method to add Menu item to the cart
        """
        
        serializer = CartSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        DELETE all Menu items created by current user
        """
        try:
            delivery_user_n = Cart.objects.filter(user=request.user)
            delivery_user_n.delete()
            return Response({'message':'Ok'},status.HTTP_204_NO_CONTENT)
        
        except Cart.DoesNotExist:
            return({'message':'Delivery Group not Found'},status.HTTP_404_NOT_FOUND)    

class OrderManagementView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    def list(self,request):            
        """
        GET method to list all the items in order for the user
        """
        if request.user.groups.filter(name='Manager').exists():
            queryset = Order.objects.select_related('delivery_crew').all()
            delivery_crew = request.query_params.get('delivery_crew')
            status = request.query_params.get('status')
            total = request.query_params.get('total')
            search = request.query_params.get('search')
            perpage = request.query_params.get('perpage',default=2)
            page = request.query_params.get('page',default=1)
            if delivery_crew:
                queryset = queryset.filter(delivery_crew__username=delivery_crew)
            if status:
                queryset = queryset.filter(status=status)
            if search:
                queryset = queryset.filter(delivery_crew__username__icontains=search)
            if total:
                queryset = queryset.filter(total__lte=total)

            paginator = Paginator(queryset,per_page=perpage)

            try:
                queryset = paginator.page(number=page)
            except EmptyPage:
                queryset = []
                                        
            serializer = OrderSerializer(queryset,many=True)
            return Response(serializer.data)
        
        elif request.user.groups.filter(name='delivery_crew').exists():
            order = Order.objects.filter(delivery_crew= self.request.user)
            # can use this if want to list all filtered order queryset = OrderItem.objects.filter(order_id__in=order)
            serializer = OrderSerializer(order,many=True)
            return Response(serializer.data)
        
        else:
            order = Order.objects.filter(user=request.user)
            queryset = OrderItem.objects.filter(order__in=order)
            serializer = OrderItemSerializer(queryset, many=True)
            return Response(serializer.data)

    def create(self, request):
        """
        POST method to create a new order for current customer which would get current cart items
        from the cart endpoint and add those items to the order items table, then deletes
        all items from the cart for this user.    
        """
        # Retrieve all cart items for the current user
        cart_items = Cart.objects.filter(user=self.request.user)
        total = self.calculate_total(cart_items)
        order = Order.objects.create(user=request.user,status=False,total=total,date=date.today())
        # Serialize cart items with 'many=True' since cart_items is a QuerySet
        
        for i in cart_items.values():
            menu_item = get_object_or_404(MenuItem,id=i['menuitem_id'])
            order_item = OrderItem.objects.create(order=order,menuitem=menu_item,quantity=i['quantity'])
            order_item.save()
        cart_items.delete()

        # Return any validation errors
        return Response({"message":"Your order has been placed."}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """
        GET method to get a single order for the same user. 
        If the order_id does not belong to the user, throw an error.
        """
        # Fetch the order associated with the user
        order = get_object_or_404(Order.objects.filter(user=request.user), pk=pk)

        # Fetch the order items related to the order
        order_items = OrderItem.objects.filter(order=order)

        if order_items.exists():
            # Serialize the order items if they exist
            serializer = OrderItemSerializer(order_items, many=True)
            return Response(serializer.data, status=200)  # HTTP 200 OK
        else:
            # If no order items are found, return a suitable message
            return Response({"detail": "No items found for this order."}, status=404)

    def partial_update(self, request, pk=None):
        """
        PATCH method to partially update an existing Order
        """
        if request.user.groups.filter(name='Manager').exists():
            serialized_item = OrderPutSerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            crew_pk = request.data.get('delivery_crew',None)
            status = request.data.get('status',None)
            order = get_object_or_404(Order, pk=pk)  # Fetch the specific menu item
            crew = get_object_or_404(User, pk=crew_pk)
            order.delivery_crew = crew
            order.status = status
            order.save()
            return Response(status=201, data={'message':str(crew.username)+' was assigned to order #'+str(order.id)})
        
        if request.user.groups.filter(name='delivery_crew').exists():
            order = get_object_or_404(Order.objects.filter(delivery_crew= self.request.user,pk=pk))
            serialized_item = OrderPutSerializerDelivery(order,data=request.data)
            serialized_item.is_valid(raise_exception=True)
            status = request.data.get('status',None)
            order.status = status
            order.save()
            return Response(status=201, data={'message':'The order status has been changed'})

        return Response({'message': 'You are not authorized'}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self,request,pk=None):
        """
        DELETE method to delete an existing Order.
        """
        if request.user.groups.filter(name='Manager').exists():
            try:
                order=get_object_or_404(Order,pk=pk)
                order.delete()
                return Response({"message":"OK"},status.HTTP_204_NO_CONTENT)
            except Order.DoesNotExist:
                return({'message':'Order not Found'},status.HTTP_404_NOT_FOUND)
            
    def calculate_total(self, cart_items):
        total = Decimal(0)
        for item in cart_items:
            total += item.price
        return total





