from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def home(request):
    return render(request, 'base.html')

def register_view(request):
    if request.user.is_authenticated: 
        return redirect('home')                # (Giriş yapmış kullanıcıyı ana sayfaya yönlendiriyoruz (Güvenlik))

    if request.method == 'POST':
        
        u_name = request.POST.get('username')         # We retrieve data using 'name' tags in HTML form.
        u_email = request.POST.get('email')                                 # (HTML formundaki 'name' etiketleriyle verileri çekiyoruz)
        u_pass = request.POST.get('password')
        u_pass_confirm = request.POST.get('password_confirm')

       
        if u_pass != u_pass_confirm:                                                 # Are the passwords the same?
            messages.error(request, 'Şifreler eşleşmiyor!')                 #( Şifreler aynı mı?)
            return render(request, 'register.html')

        if User.objects.filter(username=u_name).exists():                #Does the username already exist?
            messages.error(request, 'bu kullanıcı adı zaten alınmış!')   # (Kullanıcı adı zaten var mı?)
            return render(request, 'register.html')

        
        User.objects.create_user(username=u_name, email=u_email, password=u_pass)                       # Register the user in MSSQL.
        messages.success(request, 'Kaydınız başarıyla oluşturuldu! Şimdi giriş yapabilirsiniz.')    # (Kullanıcıyı MSSQL'e kaydet)
        return redirect('login')  # After registration, it redirects to the login page.    ( # Kayıttan sonra giriş sayfasına yönlendirir  )

    return render(request, 'register.html')

def login_view(request):
    # Giriş yapmış kullanıcıyı ana sayfaya yönlendiriyoruz (Güvenlik)
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Hoş geldin, {user.username}!")
            return redirect('home') # Ana sayfaya yönlendirir
        else:
            messages.error(request, "Hatalı kullanıcı adı veya şifre!")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "Başarıyla çıkış yaptınız.")
    return redirect('home')