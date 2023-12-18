"""
URL configuration for dj_razorpay project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from payment import views
from payment.views import TodayCollection, csrf_token
from payment.views import handle_login
from rest_framework.authtoken.views import obtain_auth_token
from payment.views import update_profile, sign_out
from payment.views import  update_user_profile
# from payment.views import UserProfileCreateView
from rest_framework.authtoken.views import obtain_auth_token
from django.views.decorators.csrf import ensure_csrf_cookie
from payment.views import get_donar_data
from payment.views import tawkto_check




urlpatterns = [
    path('admin/', admin.site.urls),
    path('handle_login/', handle_login, name='handle_login'),
    path('', views.homepage, name='index'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('create_razorpay_order/', views.create_razorpay_order, name='create_razorpay_order'),
    path('handle_data/', views.handle_data, name='handle_data'),
    path('handle_data_cash/', views.handle_data_cash, name='handle_data_cash'),
    path('today_collection/', TodayCollection.as_view(), name='today_collection'),
    path('generate_excel/', views.generate_excel, name='generate_excel'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
    path('auth/login/', obtain_auth_token, name='auth_user_login'),
    path('donar_data/', get_donar_data, name='get_donar_data'),
    path('update_profile/<int:user_id>/', update_profile, name='update_profile'),
    path('sign_out/', sign_out, name='sign_out'),
    path('update_user_profile/<int:user_id>/', update_user_profile, name='update_user_profile'),
    path('update_profile/<str:user_id>/', views.update_profile, name='update_profile'),
    path('create_user_profile/',views.create_user_profile, name='create_user_profile'),
    path('api/token/', obtain_auth_token, name='token_obtain_pair'),
    path('csrf_token/', csrf_token, name='csrf_token'),
    path('tawkto-check/', tawkto_check, name='tawkto_check'),
    
    
]
