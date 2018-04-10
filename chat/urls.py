from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^$',  views.about, name='about'),
    url(r'new/$', views.new_room, name='new_room'),
    url(r'^(?P<label>[\w-]{,50})/$', views.chat_room, name='chat_room'),
]    

