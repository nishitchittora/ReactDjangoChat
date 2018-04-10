# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, reverse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.


def user_login(request):
	if request.method == "POST":
		print(request.POST)
		username = 	request.POST.get('username')
		password = 	request.POST.get('password')
		user = authenticate(username=username, password=password)

		print(user)
		if user:
			login(request, user)
			return redirect(reverse('chat:about'))
		else:
			messages.warning(request, 'Either password or username is invalid!!')
			return redirect(reverse('core:login'))
	else:
		return render(request,'account/login.html',{}) 


def user_signup(request):
	if request.method == "POST":
		print(request.POST)
		username = 	request.POST.get('username')
		password = 	request.POST.get('password')
		confirm_password = request.POST.get('confirm_password')
		user = User.objects.filter(username=username)
		print(user)
		if not user.count():
			if password != confirm_password:
				messages.warning(request, "passwords are different!!!")
				return redirect(reverse('core:signup'))
			else:
				user = User.objects.create(username=username)
				user.set_password(password)
				user.save()
				messages.warning(request, "Signup successfully, please login")
				return redirect(reverse('chat:about'))
		else:
			messages.warning(request, 'Username already taken!!')
			return redirect(reverse('core:signup'))
	else:
		return render(request,'account/signup.html',{}) 
	



def user_signout(request):
	pass

