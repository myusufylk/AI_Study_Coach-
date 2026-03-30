from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings

import google.generativeai as genai

# Form ve Modeller
from .forms import ProfileForm
from .models import Profile, StudyPlan, Course
from .ai_service import generate_study_program

# Gemini Yapılandırması
genai.configure(api_key=settings.GOOGLE_API_KEY)

# --- ANA SAYFA ---
def home(request):
    profile = None
    program = None

    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
        latest_plan = StudyPlan.objects.filter(user=request.user).order_by('-created_at').first()
        if latest_plan:
            program = latest_plan.plan_content

    return render(request, 'dashboard.html', {
        'profile': profile,
        'program': program
    })

# --- KAYIT / GİRİŞ / ÇIKIŞ ---
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        u_name = request.POST.get('username')
        u_email = request.POST.get('email')
        u_pass = request.POST.get('password')
        u_pass_confirm = request.POST.get('password_confirm')

        if u_pass != u_pass_confirm:
            messages.error(request, 'Şifreler eşleşmiyor!')
            return render(request, 'register.html')

        if User.objects.filter(username=u_name).exists():
            messages.error(request, 'Bu kullanıcı adı zaten alınmış!')
            return render(request, 'register.html')

        user = User.objects.create_user(username=u_name, email=u_email, password=u_pass)
        Profile.objects.create(user=user)
        
        messages.success(request, 'Kaydınız başarıyla oluşturuldu! Giriş yapabilirsiniz.')
        return redirect('login')

    return render(request, 'register.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Hoş geldin, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Hatalı kullanıcı adı veya şifre!")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Başarıyla çıkış yaptınız.")
    return redirect('home')

# --- PROFİL VE AYARLAR ---
@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            form.save_m2m() 
            messages.success(request, "Profil bilgileriniz güncellendi.")
            return redirect("home")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "profile.html", {"form": form})

# --- DERS SEÇİMİ ---
@login_required
def subjects_view(request):

    if request.method == "POST":
        selected_subjects = request.POST.getlist('subject')
        try:
            profile = Profile.objects.get(user=request.user)
            profile.selected_subjects = ",".join(selected_subjects)
            profile.save()
            messages.success(request, "Ders seçimleriniz başarıyla kaydedildi!")
            return redirect('home')
        except Profile.DoesNotExist:
            messages.error(request, "Lütfen önce profil oluşturun.")
            return redirect('profile')
            
    return render(request, 'subjects.html')

    all_courses = Course.objects.all()
    # Şablonda hangilerinin seçili olduğunu bilmek için ID listesi gönderiyoruz
    selected_ids = list(profile.selected_courses.values_list('id', flat=True))

    return render(request, 'subjects.html', {
        'courses': all_courses, 
        'profile': profile,
        'selected_subjects': selected_ids
    })

# --- HAFTALIK HEDEF
@login_required
def weekly_goal_view(request):

    if request.method == "POST":
        hours = request.POST.get('hours_per_day')
        days = request.POST.get('days_per_week')
        priority = request.POST.get('priority_subject')
        note = request.POST.get('goal_note')
        
        try:
            profile = Profile.objects.get(user=request.user)
            if hours:
                profile.daily_hours = int(hours)
            if days:
                profile.weekly_study_days = int(days)
            if priority:
                profile.priority_subject = priority
            if note:
                profile.weekly_goal_note = note
                
            profile.save()
            messages.success(request, "Haftalık hedefiniz başarıyla kaydedildi!")
            return redirect('home')
        except Profile.DoesNotExist:
            messages.error(request, "Lütfen önce profil oluşturun.")
            return redirect('profile')

    return render(request, 'weekly_goal.html')


# --- AI SERVİSLERİ ---
@login_required
def ai_coach_view(request):
    response_text = ""
    if request.method == "POST":
        user_query = request.POST.get("user_query")
        full_prompt = f"Sen bir eğitim koçusun. İsmin AI Study Coach. Öğrencinin sorusu: {user_query}"

        try:
            model = genai.GenerativeModel('gemini-2.0-flash')
            ai_response = model.generate_content(full_prompt)
            response_text = ai_response.text
        except Exception as e:
            response_text = f"AI cevap üretirken bir hata oluştu: {str(e)}"

    return render(request, 'ai_coach.html', {'response': response_text})

@login_required
def generate_program(request):
    try:
        profile = Profile.objects.get(user=request.user)
        program = generate_study_program(profile.target_exam, profile.daily_hours)

        if '"error":' in program or "⚠️" in program:
            messages.error(request, f"AI Programı oluşturamadı: {program}")
            return redirect("home")

        StudyPlan.objects.filter(request.user == user).delete() # Yanlış filtreyi düzelttim
        StudyPlan.objects.filter(user=request.user).delete()

        StudyPlan.objects.create(
            user=request.user,
            plan_content=program
        )

        messages.success(request, "Haftalık programın başarıyla güncellendi!")
        return redirect("home")

    except Profile.DoesNotExist:
        messages.error(request, "Önce profil bilgilerini doldurmalısın.")
        return redirect("profile")
    except Exception as e:

        messages.error(request, f"Program oluşturulurken hata oluştu: {str(e)}")
        return redirect("home")

@login_required
def lesson_watch(request):
    # Dummy veriler ile arayüzün çalışması sağlanır
    context = {
        'lesson': {'name': 'Matematik'},
        'topic': {'title': 'Türev - Kurallar'},
        'video': {'url': 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'id': 1},
        'videos': [
            {'id': 1, 'title': 'Türev Nedir?', 'duration': '10:05'},
            {'id': 2, 'title': 'Çarpım Kuralı', 'duration': '12:30'},
            {'id': 3, 'title': 'Bölüm Kuralı', 'duration': '15:45'}
        ]
    }
    return render(request, 'lesson_watch.html', context)
