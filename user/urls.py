from django.urls import path
from .import views

app_name = 'user'

urlpatterns = [
    path('', views.loginPage, name="login"),
    path('signUp/', views.signUpPage, name="signUp"),
    path('getOTP/', views.getOTP, name="getCode"),
    path('resetPassword/', views.resetPass, name="resetPass"),
    path('account/', views.accountPage, name="account"),
]
