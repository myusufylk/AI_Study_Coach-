from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings

from google import genai

from .forms import ProfileForm
from .models import Profile, StudyPlan
from .ai_service import generate_study_program

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

        User.objects.create_user(
            username=u_name,
            email=u_email,
            password=u_pass
        )

        messages.success(request, 'Kaydınız başarıyla oluşturuldu! Şimdi giriş yapabilirsiniz.')
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


@login_required
def profile_view(request):

    profile = Profile.objects.filter(user=request.user).first()

    if request.method == "POST":

        form = ProfileForm(request.POST, instance=profile)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()

            messages.success(request, "Profil başarıyla kaydedildi.")
            return redirect("home")

    else:
        form = ProfileForm(instance=profile)

    return render(request, "profile.html", {"form": form})


@login_required
def subjects_view(request):
    return render(request, 'subjects.html')


@login_required
def weekly_goal_view(request):
    return render(request, 'weekly_goal.html')


@login_required
def ai_coach_view(request):

    response_text = ""

    if request.method == "POST":

        user_query = request.POST.get("user_query")

        full_prompt = f"""
Sen bir eğitim koçusun.
İsmin AI Study Coach.

Öğrencinin sorusu:
{user_query}
"""

        try:
            client = genai.Client(api_key=settings.GOOGLE_API_KEY)

            ai_response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=full_prompt
            )

            # güvenli okuma
            response_text = getattr(ai_response, "text", "AI cevap üretemedi.")

        except Exception as e:
            response_text = f"AI cevap üretirken bir hata oluştu: {str(e)}"

    return render(request, 'ai_coach.html', {'response': response_text})


@login_required
def generate_program(request):

    try:
        profile = Profile.objects.get(user=request.user)

        program = generate_study_program(
            profile.target_exam,
            profile.daily_hours
        )

        # PLANI KAYDET (Dashboard'da göstermek için)
        StudyPlan.objects.create(
            user=request.user,
            plan_content=program
        )

        return render(request, "program.html", {
            "program": program
        })

    except Profile.DoesNotExist:
        messages.error(request, "Önce profil bilgilerini doldurmalısın.")
        return redirect("profile")

    except Exception as e:
        messages.error(request, f"Program oluşturulurken hata oluştu: {str(e)}")
        return redirect("home")