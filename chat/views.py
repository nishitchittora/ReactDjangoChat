# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import transaction
from django.shortcuts import render, reverse, redirect

import haikunator
from .models import *
# Create your views here.

def about(request):
	return render(request, "chat/about.html")

def new_room(request):
    new_room = None
    while not new_room:
        with transaction.atomic():
            label = haikunator.haikunate()
            if Room.objects.filter(label=label).exists():
                continue
            new_room = Room.objects.create(label=label)
    return redirect(reverse('chat:chat_room', kwargs={'label':label}))


def chat_room(request, label):
    room, created = Room.objects.get_or_create(label=label)
    messages = reversed(room.messages.order_by('-timestamp')[:50])
    return render(request, "chat/room.html", {
        'room': room,
        'messages': messages,
    })
