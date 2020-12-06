from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('users/sign_up.html', views.sign_up, name='sign_up'),
]
