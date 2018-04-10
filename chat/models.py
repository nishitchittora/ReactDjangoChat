# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from model_utils.models import TimeStampedModel
from django.utils.six import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

# Create your models here.

@python_2_unicode_compatible
class Room(TimeStampedModel):
    title = models.CharField(_('Chat Title'), max_length=255, blank=True, null=True)
    label = models.SlugField(unique=True)

    def __unicode__(self):
    	return self.label

    def __str__(self):
    	return self.label


@python_2_unicode_compatible
class Message(TimeStampedModel):
    room = models.ForeignKey(Room, blank=True, null=True, related_name='messages')
    handle = models.TextField()
    message = models.TextField(_('Message'))
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    def __unicode__(self):
        return '[{timestamp}] {handle}: {message}'.format(**self.as_dict())
    
    def __str__(self):
    	return '[{timestamp}] {handle}: {message}'.format(**self.as_dict())


    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime('%b %-d %-I:%M %p')
    
    def as_dict(self):
        return {'handle': self.handle, 'message': self.message, 'timestamp': self.formatted_timestamp}



