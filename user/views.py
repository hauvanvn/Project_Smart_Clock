from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import User, OtpToken
from .forms import SignupForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from .utils import sendOtp
from django.utils import timezone
from django.utils.timesince import timesince

# Create your views here.
def loginPage(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get('user')
        password = request.POST.get('pass')

        user = authenticate(request, username=username, password=password)
        if user is None or not user.is_active:
            messages.warning(request, 'Username or Password is incorrect.')
            return redirect('users:login')
        else:
            login(request, user)
            return redirect('home')

    return render(request, 'user/login.html')

def signUpPage(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get('user')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if User.objects.filter(username=username).exists():
            messages.warning(request, 'Username already been used!')
            return redirect('users:signup')
        if pass1 != pass2:
            messages.warning(request, 'Username already been used!')
            return redirect('users:signnup')
        
        form = SignupForm({
            'username': username, 
            'password1': pass1, 
            'password2': pass2, 
            'email': email
            })
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('users:login')
        else:
            print(form.errors.as_text())
            messages.warning(request, "Create new account fail!")
            return redirect('users:signup')
        
    return render(request, 'user/signup.html')

def getOTP(request):
    if request.method == "POST":
        return redirect('user:resetPass')
    return render(request, 'user/receiveOTP.html')

def resetPass(request):
    return render(request, 'user/resetPass.html')

def logoutPage(request):
    logout(request)
    return redirect('users:login')

def accountPage(request):
    return render(request, 'user/account.html')