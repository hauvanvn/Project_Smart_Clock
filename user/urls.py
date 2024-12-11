from django.urls import path
from .import views

app_name = 'users'

urlpatterns = [
    path('', views.loginPage, name="login"),
    path("signup/", views.signUpPage, name="signup"),
    path('getcode/', views.getOTP, name="resetPass"),
    path('resetPass/', views.resetPass, name="resetPass_1"),
    path('logout/', views.logoutPage, name='logout'),
    path('profile/', views.accountPage, name='profile'),
]
