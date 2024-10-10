from django.contrib import admin
from django.urls import path,include
from .views import MenuItemsView,ManagerUsersView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('menu-items',MenuItemsView.as_view({'get':'list','post':'create'})),
    path('menu-items/<int:pk>',MenuItemsView.as_view({'get':'retrieve','put':'update','patch':'partial_update','delete':'destroy'})),
    path('groups/manager/users',ManagerUsersView.as_view({'get':'list','post':'create'})),
    path('groups/manager/users/<int:pk>',ManagerUsersView.as_view({'delete':'destroy'})),
]