from django.urls import path
from . import views
 
urlpatterns = [
    path('',views.index, name='index'),
    path('counter',views.counter, name='counter'),
    path('register',views.register, name='register'),
    path('login',views.login, name='login'),
    path('add_customer/', views.add_customer, name='add_customer'),
     path('view_customers/', views.view_customers, name='view_customers'),
 ]
 