"""
Views — HTTP istek/cevap katmanı.

Tüm AI mantığı ai_service modülüne devredilmiştir.
Bu dosya yalnızca form işleme, yetkilendirme ve şablon
render işlemlerinden sorumludur.
"""

import json
import logging

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import ProfileForm
from .models import Profile, StudyPlan, Course
from .ai_service import generate_study_program, ask_ai_coach

logger = logging.getLogger(__name__)


# ── Yardımcılar ─────────────────────────────────────────────────────────────
def _get_profile_or_redirect(request):
    """
    Aktif kullanıcının profilini döner.

    Returns:
        (Profile, None)  — başarılı
        (None, redirect)  — profil yoksa hazır redirect response
    """
    try:
        return Profile.objects.get(user=request.user), None
    except Profile.DoesNotExist:
        messages.error(request, "Lütfen önce profil oluşturun.")
        return None, redirect("profile")
    except Exception:
        logger.exception("DB error fetching profile for user=%s", request.user)
        messages.error(request, "Profil bilgileri alınırken bir hata oluştu.")
        return None, redirect("home")


def _safe_int(value, field_label):
    """
    String → int dönüşümü yapar.

    Returns:
        (int, None)   — başarılı
        (None, str)   — hata mesajı
    """
    try:
        result = int(value)
        return result, None
    except (TypeError, ValueError):
        return None, f"Geçersiz {field_label} değeri girdiniz."


# ─────────────────────────────────────────────────────────────────────────────
# ANA SAYFA
# ─────────────────────────────────────────────────────────────────────────────
def home(request):
    profile = None
    program = None

    if request.user.is_authenticated:
        try:
            profile = Profile.objects.filter(user=request.user).first()
            latest_plan = (
                StudyPlan.objects.filter(user=request.user)
                .order_by("-created_at")
                .first()
            )
            if latest_plan:
                program = latest_plan.plan_content
        except Exception:
            logger.exception("Error loading home data for user=%s", request.user)
            messages.error(request, "Veriler yüklenirken bir sorun oluştu.")

    return render(request, "dashboard.html", {
        "profile": profile,
        "program": program,
    })


# ─────────────────────────────────────────────────────────────────────────────
# KAYIT / GİRİŞ / ÇIKIŞ
# ─────────────────────────────────────────────────────────────────────────────
def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method != "POST":
        return render(request, "register.html")

    u_name = request.POST.get("username", "").strip()
    u_email = request.POST.get("email", "").strip()
    u_pass = request.POST.get("password", "")
    u_pass_confirm = request.POST.get("password_confirm", "")

    if not u_name or not u_pass:
        messages.error(request, "Kullanıcı adı ve şifre zorunludur!")
        return render(request, "register.html")

    if u_pass != u_pass_confirm:
        messages.error(request, "Şifreler eşleşmiyor!")
        return render(request, "register.html")

    if User.objects.filter(username=u_name).exists():
        messages.error(request, "Bu kullanıcı adı zaten alınmış!")
        return render(request, "register.html")

    try:
        user = User.objects.create_user(
            username=u_name, email=u_email, password=u_pass,
        )
        Profile.objects.create(user=user)
        messages.success(
            request, "Kaydınız başarıyla oluşturuldu! Giriş yapabilirsiniz.",
        )
        return redirect("login")
    except Exception:
        logger.exception("Error creating user account: %s", u_name)
        messages.error(
            request,
            "Kayıt oluşturulurken bir sorun oluştu. Lütfen tekrar deneyin.",
        )
        return render(request, "register.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Hoş geldin, {user.username}!")
            return redirect("home")
        else:
            messages.error(request, "Hatalı kullanıcı adı veya şifre!")
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "Başarıyla çıkış yaptınız.")
    return redirect("home")


# ─────────────────────────────────────────────────────────────────────────────
# PROFİL
# ─────────────────────────────────────────────────────────────────────────────
@login_required
def profile_view(request):
    try:
        profile, _ = Profile.objects.get_or_create(user=request.user)
    except Exception:
        logger.exception("Error accessing profile for user=%s", request.user)
        messages.error(request, "Profil bilgileri yüklenemedi.")
        return redirect("home")

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            try:
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                form.save_m2m()
                messages.success(request, "Profil bilgileriniz güncellendi.")
                return redirect("home")
            except Exception:
                logger.exception("Error saving profile for user=%s", request.user)
                messages.error(
                    request,
                    "Profil kaydedilirken bir hata oluştu. Lütfen tekrar deneyin.",
                )
    else:
        form = ProfileForm(instance=profile)

    return render(request, "profile.html", {"form": form})


# ─────────────────────────────────────────────────────────────────────────────
# DERS SEÇİMİ
# ─────────────────────────────────────────────────────────────────────────────
@login_required
def subjects_view(request):
    if request.method == "POST":
        selected_subjects = request.POST.getlist("subject")
        profile, resp = _get_profile_or_redirect(request)
        if resp:
            return resp

        try:
            profile.selected_subjects = ",".join(selected_subjects)
            profile.save()
            messages.success(request, "Ders seçimleriniz başarıyla kaydedildi!")
            return redirect("home")
        except Exception:
            logger.exception("Error saving subjects for user=%s", request.user)
            messages.error(request, "Ders seçimleri kaydedilirken bir hata oluştu.")
            return redirect("home")

    # GET — ders listesi sayfası
    try:
        profile = Profile.objects.filter(user=request.user).first()
        all_courses = Course.objects.all()
        selected_ids = []
        if profile and hasattr(profile, "selected_courses"):
            selected_ids = list(
                profile.selected_courses.values_list("id", flat=True)
            )
    except Exception:
        logger.exception("Error loading subjects page for user=%s", request.user)
        all_courses = []
        profile = None
        selected_ids = []

    return render(request, "subjects.html", {
        "courses": all_courses,
        "profile": profile,
        "selected_subjects": selected_ids,
    })


# ─────────────────────────────────────────────────────────────────────────────
# HAFTALIK HEDEF
# ─────────────────────────────────────────────────────────────────────────────
@login_required
def weekly_goal_view(request):
    if request.method != "POST":
        return render(request, "weekly_goal.html")

    profile, resp = _get_profile_or_redirect(request)
    if resp:
        return resp

    hours = request.POST.get("hours_per_day")
    days = request.POST.get("days_per_week")
    priority = request.POST.get("priority_subject")
    note = request.POST.get("goal_note")

    if hours:
        val, err = _safe_int(hours, "saat")
        if err:
            messages.error(request, err)
            return render(request, "weekly_goal.html")
        profile.daily_hours = val

    if days:
        val, err = _safe_int(days, "gün")
        if err:
            messages.error(request, err)
            return render(request, "weekly_goal.html")
        profile.weekly_study_days = val

    if priority:
        profile.priority_subject = priority
    if note:
        profile.weekly_goal_note = note

    try:
        profile.save()
        messages.success(request, "Haftalık hedefiniz başarıyla kaydedildi!")
        return redirect("home")
    except Exception:
        logger.exception("Error saving weekly goal for user=%s", request.user)
        messages.error(
            request,
            "Haftalık hedef kaydedilirken bir hata oluştu. Lütfen tekrar deneyin.",
        )
        return redirect("home")


# ─────────────────────────────────────────────────────────────────────────────
# AI SERVİSLERİ
# ─────────────────────────────────────────────────────────────────────────────
@login_required
def ai_coach_view(request):
    """AI koç — tüm Groq mantığı ai_service.ask_ai_coach()'a devredildi."""
    response_text = ""

    if request.method == "POST":
        user_query = request.POST.get("user_query", "").strip()

        if not user_query:
            messages.warning(request, "Lütfen bir soru yazın.")
        else:
            response_text = ask_ai_coach(user_query)

    return render(request, "ai_coach.html", {"response": response_text})


@login_required
def generate_program(request):
    """Haftalık program oluştur — AI mantığı ai_service'e devredildi."""
    profile, resp = _get_profile_or_redirect(request)
    if resp:
        return resp

    course_names = [c.name for c in profile.selected_courses.all()]
    try:
        program = generate_study_program(profile.target_exam, profile.daily_hours, course_names)
    except Exception:
        logger.exception("Unexpected error calling generate_study_program")
        messages.error(request, "Program oluşturulurken beklenmeyen bir hata oluştu.")
        return redirect("home")

    # JSON'ı parse et ve error kontrolü yap
    try:
        # Markdown bloklarını temizle (```json ... ```)
        cleaned_program = program.strip()
        if cleaned_program.startswith("```json"):
            cleaned_program = cleaned_program[7:]
        elif cleaned_program.startswith("```"):
            cleaned_program = cleaned_program[3:]
        
        if cleaned_program.endswith("```"):
            cleaned_program = cleaned_program[:-3]
            
        cleaned_program = cleaned_program.strip()
        
        program_data = json.loads(cleaned_program)
        
        if isinstance(program_data, dict) and "error" in program_data:
            error_msg = program_data.get("error", "Bilinmeyen bir hata oluştu.")
            messages.error(request, f"AI programı oluşturamadı: {error_msg}")
            return redirect("home")
    except json.JSONDecodeError:
        logger.error("Invalid JSON response from generate_study_program: %s", program)
        messages.error(request, "Program formatı geçersiz. Lütfen tekrar deneyin.")
        return redirect("home")

    try:
        StudyPlan.objects.filter(user=request.user).delete()
        StudyPlan.objects.create(user=request.user, plan_content=cleaned_program)
    except Exception:
        logger.exception("DB error saving study plan for user=%s", request.user)
        messages.error(request, "Program kaydedilirken bir sorun oluştu.")
        return redirect("home")

    messages.success(request, "Haftalık programın başarıyla güncellendi!")
    return redirect("home")


# ─────────────────────────────────────────────────────────────────────────────
# DERS İZLEME
# ─────────────────────────────────────────────────────────────────────────────
@login_required
def lesson_watch(request):
    """Dummy veriler ile arayüzün çalışması sağlanır."""
    context = {
        "lesson": {"name": "Matematik"},
        "topic": {"title": "Türev - Kurallar"},
        "video": {
            "url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "id": 1,
        },
        "videos": [
            {"id": 1, "title": "Türev Nedir?", "duration": "10:05"},
            {"id": 2, "title": "Çarpım Kuralı", "duration": "12:30"},
            {"id": 3, "title": "Bölüm Kuralı", "duration": "15:45"},
        ],
    }
    return render(request, "lesson_watch.html", context)
