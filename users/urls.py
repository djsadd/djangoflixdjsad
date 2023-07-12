from django.contrib import admin
from django.urls import path, include
from .views import HomeNetflixView, UserRegisterView, EmailVerificationView, UserLogin, logout_user, UserProfileView, UserProfiles, remove, login

urlpatterns = [
    path('', HomeNetflixView.as_view(), name='start'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('log/<int:pk>', login, name='log'),
    path('logout/', logout_user, name='logout'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='profile'),
    path('profiles/', UserProfiles.as_view(), name='profiles'),
    path('remove/<int:pk>', remove, name='remove'),
    path('verify/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name='verify'),
]