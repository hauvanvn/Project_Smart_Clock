from django.shortcuts import render, redirect

# Create your views here.
def loginPage(request):
    if request.method == "POST":
        return redirect('login')
    return render(request, 'user/login.html')

def signUpPage(request):
    return render(request, 'user/signup.html')

def getOTP(request):
    if request.method == "POST":
        return redirect('user:resetPass')
    return render(request, 'user/receiveOTP.html')

def resetPass(request):
    return render(request, 'user/resetPass.html')

def accountPage(request):
    return render(request, 'user/account.html')