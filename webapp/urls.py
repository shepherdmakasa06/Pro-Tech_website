from django.urls import path
from . import views
 
urlpatterns = [
    path('',views.index, name='index'),
    path('counter',views.counter, name='counter'),
    path('register',views.register, name='register'),
    path('login',views.login, name='login'),
    path('add_customer/', views.add_customer, name='add_customer'),
    path('view_customers/', views.view_customers, name='view_customers'),
    path('send-verification-email', views.send_verification_email, name='send_verification_email'),
    path('verify-email-code', views.verify_email_code, name='verify_email_code'),
    path('change_password/', views.change_password, name='change_password'),
    path('save_receipt/', views.save_receipt, name='save_receipt'),
    path('user_list/', views.user_list, name='user_list'),
    path('toggle_user_active/<int:user_id>/', views.toggle_user_active, name='toggle_user_active'),
 ]
 