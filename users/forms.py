from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.conf import settings
from django import forms
import uuid
from datetime import timedelta

from django.forms import ModelForm
from django.utils.timezone import now
from .models import EmailVerification, User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={"class": "emailField", "placeholder": "Email"}))
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={"class": "emailField", "placeholder": "Username"}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'id': 'password', 'placeholder': 'Password',
    }))
    password2 = forms.CharField(label='Password2', widget=forms.PasswordInput(attrs={
        'id': 'password', 'placeholder': 'Password',
    }))
    date_birthday = forms.DateTimeField(label='start', widget=forms.DateInput(attrs={"type": "date", "id": "start", "value": "2023-07-22"}))

    class Meta(UserCreationForm):
        model = User
        fields = ('email', 'username', 'password1', 'password2', 'date_birthday')

    def save(self, commit=True):
        print('save!!')
        context = super(UserRegistrationForm, self).save(commit=commit)
        print(context)
        tm = now()
        record = EmailVerification.objects.create(user=context, code=uuid.uuid4(), created=tm, expiration=tm+timedelta(hours=48))
        record.send_verification_email()
        return context


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={"class": "emailField", "placeholder": "Username"}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'name': 'password', 'id': 'password', 'placeholder': 'Password',
    }))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserUpdateForm(UserChangeForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'email'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"class": "email"}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input', }), required=False)

    class Meta:
        model = User
        fields = ('email', 'phone', 'image')


class UserProfilesAddForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "email"}))

    class Meta:
        model = User
        fields = ['username']