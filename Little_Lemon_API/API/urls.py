from django.contrib import admin
from django.urls import path,include
from .views import MenuItemsView,ManagerUsersView,DeliveryUsersView,CartManagementView,OrderManagementView

urlpatterns = [
    path('menu-items',MenuItemsView.as_view({'get':'list','post':'create'})),
    path('menu-items/<int:pk>',MenuItemsView.as_view({'get':'retrieve','put':'update','patch':'partial_update','delete':'destroy'})),
    path('groups/manager/users',ManagerUsersView.as_view({'get':'list','post':'create'})),
    path('groups/manager/users/<int:pk>',ManagerUsersView.as_view({'delete':'destroy'})),
    path('groups/delivery-crews/users',DeliveryUsersView.as_view({'get':'list','post':'create'})),
    path('groups/delivery-crews/users/<int:pk>',DeliveryUsersView.as_view({'delete':'destroy'})),
    path('cart/menu-items',CartManagementView.as_view({'get':'list','post':'create','delete':'destroy'})),
    path('orders',OrderManagementView.as_view({'get':'list','post':'create'})),
    path('orders/<int:pk>',OrderManagementView.as_view({'get':'retrieve','patch':'partial_update','delete':'destroy'})),
]