from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, get_user_model
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .forms import SignUpForm, ProfileForm
from .models import Profile
from datetime import date
from django.views.generic import TemplateView
from django.http.request import HttpRequest
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()


def home(request):
    return render(request, 'ota_chat/home.html')


def sign_up(request):
    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if signup_form.is_valid() and profile_form.is_valid():
            username = signup_form.cleaned_data.get('username')
            email = signup_form.cleaned_data.get('email')
            password = signup_form.cleaned_data.get('password1')
            geneder = profile_form.cleaned_data.get('gender')
            birth_year = profile_form.cleaned_data.get('birth_year')
            birth_month = profile_form.cleaned_data.get('birth_month')
            birth_day = profile_form.cleaned_data.get('birth_day')

            user = User.objects.create_user(
                username, email, password)
            user.profile.gender = geneder
            if birth_day and birth_month and birth_year:
                birth_date = date(int(birth_year), int(
                    birth_day), int(birth_month)).isoformat()
                user.profile.birth_date = birth_date
            user.save()

            user = authenticate(request, username=username,
                                password=password)
            auth_login(request, user,
                       backend='django.contrib.auth.backends.ModelBackend')
            messages.add_message(request, messages.SUCCESS, 'ユーザー登録が完了しました．')
            return redirect('home')
    else:
        signup_form = SignUpForm()
        profile_form = ProfileForm()

    context = {
        'signup_form': signup_form,
        'profile_form': profile_form,
    }
    return render(request, 'users/sign_up.html', context)


class Login(LoginView):
    """ログインページの操作を記述"""
    form_class = LoginForm
    template_name = 'users/login.html'


class Logout(LoginRequiredMixin, LogoutView):
    """ログアウト画面の操作を記述"""
    template_name = 'users/login.html'
