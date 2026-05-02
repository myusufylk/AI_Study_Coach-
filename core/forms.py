from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['target_exam', 'daily_hours']
        labels = {
            'target_exam': 'Haftalık Hedef',
            'daily_hours': 'Günlük Çalışma Saati',
        }