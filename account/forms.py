from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Profile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("A user with that username already exists.")
        return username



class ChangeUserData(UserChangeForm):
    password = None
    first_name = forms.CharField(max_length=20, required=False)
    last_name = forms.CharField(max_length=20, required=False)
    phone_number = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        if commit:
            user.save()
            user.profile.phone_number = self.cleaned_data['phone_number']
            user.profile.save()
        return user
