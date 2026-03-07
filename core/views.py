from django.shortcuts import render

def home(request):
    return render(request, 'base.html')

def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    return render(request, 'register.html')