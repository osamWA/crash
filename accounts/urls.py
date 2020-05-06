from django.urls import path
from . import views
urlpatterns = [
    
    path('',views.home,name='home'),
    path('customers/<str:pk>',views.customers,name='customers'),
    path('Login/',views.Login,name='Login'),
    path('User/',views.UserPage,name='User'),
    path('Logout/',views.Logout,name='Logout'),
    path('SignUp/',views.SignUp,name='SignUp'),
    path('products/',views.products, name='products'),
    path('allCustomer/',views.allCustomers, name='allCustomers'),
    path('allOrders/',views.allOrders, name='allOrders'),
    path('orderHistory/<str:pk>',views.orderHistory, name='orderHistory'),

#for Products CURD
    path('create_products/',views.create_products, name='create_products'),
    path('update_products/<str:pk>',views.update_products, name='update_products'),
    path('delete_products/<str:pk>',views.delete_products, name='delete_products'),

#for Customers CURD   
    path('create_customer/',views.create_customer, name='create_customer'),
    path('update_customer/<str:pk>',views.update_customer, name='update_customer'),
    path('delete_customer/<str:pk>',views.delete_customer, name='delete_customer'),
    path('CustomerProductSearch/<str:pk>/<str:kw>',views.CustomerProductSearch, name='CustomerProductSearch'),

#for Orders CURD
    path('create_orders/',views.create_orders, name='create_orders'),
    path('update_orders/<str:pk>',views.update_orders, name='update_orders'),
    path('delete_orders/<str:pk>',views.delete_orders, name='delete_orders'),
]

