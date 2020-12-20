from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('users/sign_up.html', views.sign_up, name='sign_up'),
    path('', views.home, name='home'),
    path('users/login.html', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
]
