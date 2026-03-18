from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, DailyLog

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose another.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['gender', 'age', 'height', 'weight', 'lifestyle', 'region_preference', 'fasting_mode',
                  'has_diabetes', 'has_hypertension', 'has_heart_disease', 'has_celiac', 'has_lactose_intolerance']

class DailyLogForm(forms.ModelForm):
    class Meta:
        model = DailyLog
        fields = ['food_item', 'quantity_g']
