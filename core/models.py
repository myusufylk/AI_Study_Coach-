from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField(max_length=100)
    video_url = models.URLField(blank=True, null=True) # Videoda bazı derslerin linki yoktu, hata vermesin
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    target_exam = models.CharField(max_length=100)
    daily_hours = models.IntegerField(default=4)
    # YENİ: Kullanıcının seçtiği dersleri veritabanında tutmak için ManyToMany ekledik
    selected_courses = models.ManyToManyField(Course, blank=True)
    weekly_goal = models.TextField(blank=True, null=True, verbose_name="Haftalık Hedef")

    def __str__(self):
        return self.user.username

class StudyPlan(models.Model):
    # Burada satır başı (indent) hatasını düzelttim:
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan_content = models.TextField() # AI'dan gelen uzun metin buraya yazılacak
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} study plan - {self.created_at.strftime('%d/%m/%Y')}"