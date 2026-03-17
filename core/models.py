from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    target_exam = models.CharField(max_length=100)

    daily_hours = models.IntegerField(default=4)

    def __str__(self):
        return self.user.username


class Course(models.Model):

    name = models.CharField(max_length=100)

    video_url = models.URLField()

    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class StudyPlan(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    plan_content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} study plan"