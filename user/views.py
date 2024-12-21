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
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        username = request.POST.get('user')

        user_exist = User.objects.filter(username=username).exists()
        if (not user_exist):
            messages.warning(request, 'Wrong Username.')
            return redirect('users:resetPass')
        else:
            request.session['username'] = username
            user = User.objects.get(username=username)
            sendOtp(user)
            return redirect('users:resetPass_1')

    return render(request, 'user/receiveOTP.html')

def resetPass(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.session['username']
        password1 = request.POST.get('pass1')
        password2 = request.POST.get('pass2')
        code = request.POST.get('otp')

        user = User.objects.get(username=username)
        otp = OtpToken.objects.filter(user=user).last()
        
        if otp.otp_expired_at > timezone.now():
            if(password1 != password2):
                messages.warning(request, 'Password do not match.')
                return redirect('users:resetPass_1')
            elif code != otp.otp_code:
                messages.warning(request, 'Wrong otp.')
                return redirect('users:resetPass_1')
            else:
                user.set_password(password2)
                user.save()
                messages.success(request, 'Successfully change password for: ' + username + '.')
                return redirect('users:login')
        else:
            messages.warning(request, 'OTP has expired.')
            return redirect('users:resetPass')
        
    return render(request, 'user/resetPass.html')

def logoutPage(request):
    logout(request)
    return redirect('users:login')

@login_required(login_url='users:login')
def accountPage(request):
    user = request.user

    if request.method == "POST":
        # Change username
        if "change_username" in request.POST:
            new_name = request.POST.get("new_username")
            if User.objects.filter(username=new_name).exists():
                messages.error(request, "Username existed!")
                return redirect('users:profile')
            
            user.username = new_name
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Change username successful!")
            return redirect('users:profile')
        # Change pass
        elif "change_pass" in request.POST:
            oldPass = request.POST.get("origin_pass")
            newPass1 = request.POST.get("new_pass1")
            newPass2 = request.POST.get("new_pass2")

            if user.check_password(oldPass):
                if newPass1 == newPass2:
                    user.set_password(newPass1)
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, "Change password successful!")
                    return redirect('users:profile')
                else:
                    messages.warning(request, "New password not match to Verify password!")
                    return redirect('users:profile')
            else:
                messages.warning(request, "Your old password is not correct!")
                return redirect('users:profile')
        # Change avarta
        elif "change_avarta" in request.POST:
            avatar = request.FILES['img']
            user.avatar = avatar
            user.save()
            messages.success(request, "Change avatar successful!")
            return redirect('users:profile')

    return render(request, 'user/account.html', {"user": user})