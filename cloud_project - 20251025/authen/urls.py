from django.urls import path, include
from django.contrib.auth import views as auth_views
from authen.views import LoginView, LogoutView, sign_up

urlpatterns = [
    path('', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('sign_up/', sign_up, name="sign_up"),
]