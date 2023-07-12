from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from .forms import UserRegistrationForm, UserLoginForm, UserUpdateForm, UserProfilesAddForm
from .models import User, EmailVerification
# Create your views here.


class HomeNetflixView(TemplateView):
    model = EmailVerification
    template_name = 'users/index.html'
    success_url = reverse_lazy('register')


class UserRegisterView(CreateView):
    form_class = UserRegistrationForm
    model = User
    template_name = 'users/register.html'
    success_message = 'Вы успешно зарегестрировались'
    success_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            dt = User.objects.filter(email=request.POST['email'])
            if dt:
                form.add_error('email', "Почта уже занята")
                return render(request, self.template_name, {"form": form})
            form.save()
            return redirect('login')
        else:
            context = {
                'form': form
            }
        return render(request, self.template_name, context=context)


class EmailVerificationView(TemplateView):
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        return redirect('home')


class UserLogin(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm


def login(request, pk):
    user = request.user.get_children().get(pk=pk)
    auth.login(request, user)
    return redirect('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class UserProfileView(UpdateView):
    model = User
    template_name = 'users/profile.html'
    form_class = UserUpdateForm

    def get_success_url(self):
        return reverse_lazy('profile', args=(self.object.id,))


class UserProfiles(CreateView):
    template_name = 'users/profiles.html'
    model = User
    form_class = UserProfilesAddForm

    def get(self, request, *args, **kwargs):
        context = {'children': request.user.get_children(), 'form': self.form_class}
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            nu = form.save()
            request.user.children.add(nu)
            request.user.save()

        return redirect('profiles')


def remove(request, pk):
    request.user.children.get(pk=pk).delete()
    return redirect('profiles')

