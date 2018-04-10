from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
from allauth.account.views import LoginView,SignupView, LogoutView
from .views import user_login, user_signup, user_signout

urlpatterns = [
    url(r'^login/$', user_login, name="login"),
    url(r'^signup/$', user_signup, name="signup"),
    url(r'^signout/$', user_signout, name="signout"),
]    

