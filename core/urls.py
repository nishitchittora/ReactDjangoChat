from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
from allauth.account.views import LoginView,SignupView, LogoutView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^signup/$', SignupView.as_view(), name="signup"),
    url(r'^signout/$', LogoutView.as_view(), name="signout"),
]    

