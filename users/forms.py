from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Profile
from datetime import datetime

User = get_user_model()


class SignUpForm(UserCreationForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    if password != password_confirm:
        error_message_in_password = "パスワードが一致しません．"

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        del self.fields['password1']
        del self.fields['password2']

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'username', 'placeholder': 'ユーザー名'}),
            'email': forms.TextInput(attrs={'class': 'email', 'placeholder': 'E-mail'}),
            'password': forms.PasswordInput(attrs={'class': 'password', 'placeholder': 'パスワード'}),
        }


class ProfileForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('1', '女性'),
        ('2', '男性'),
    ]

    gender = forms.ChoiceField(
        widget=forms.RadioSelect, choices=GENDER_CHOICES, required=True)

    class DateFunction():
        def make_select_object(self, from_x, to_y, dates, increment=True):
            if increment:
                for i in range(from_x, to_y):
                    dates.append([i, i])  # dates配列に要素を追加
            else:
                for i in range(from_x, to_y, -1):
                    dates.append([i, i])
            return dates

        def make_select_field(self, select_object):
            dates_field = forms.ChoiceField(
                widget=forms.Select, choices=select_object, required=False)
            return dates_field

    years = [["", ""]]
    current_year = datetime.now().year
    dates_instance = DateFunction()
    years = dates_instance.make_select_object(
        current_year, current_year-80, years, increment=False)
    birth_year = dates_instance.make_select_field(years)

    months = [["", ""]]
    months = dates_instance.make_select_object(1, 13, months)
    birth_month = dates_instance.make_select_field(months)

    days = [["", ""]]
    days = dates_instance.make_select_object(1, 32, days)
    birth_day = dates_instance.make_select_field(days)

    class Meta:
        model = Profile
        fields = ('gender', 'birth_year', 'birth_month', 'birth_day')
        # ここにウィジェットを追加．
        widgets = {
            'gender': forms.RadioSelect(attrs={'class': 'gender_choices'}),
            'birth_year': forms.Select(attrs={'class': 'birth_year_select'}),
            'birth_month': forms.Select(attrs={'class': 'birth_month_select'}),
            'birth_day': forms.Select(attrs={'class': 'birth_day_select'}),
        }
