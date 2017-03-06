from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import logging
# Create your models here.

log = logging.getLogger(__name__)

class Registration(models.Model):
    user = models.OneToOneField(User)
    
    comment = models.CharField(max_length=35, null=True, default=None,blank=True)

    def __str__(self):
        return self.title


class EmailThread(models.Model):
        
	text_doc = models.TextField()

class KnowledgeSource(models.Model):
        
	source_doc = models.TextField()



class Session_log(models.Model):
	user = models.ForeignKey(User)
	time_action = models.DateTimeField(default=timezone.now)
	START_ACTION = '_start'
    	END_ACTION = '_end'
	ACTION_CHOICES = (
		(START_ACTION, '_start'),
		(END_ACTION,'_end'),
	)
	session_action = models.CharField(choices = ACTION_CHOICES, default = START_ACTION ,max_length=255)


class Questions(models.Model):
	#edit to allow null , yes , no
        answer =  models.CharField(max_length=35, null=True, default=None,blank=True)
	session = models.ForeignKey(Session_log)

class UserConsent(models.Model):
	user = models.ForeignKey(User)
	session = models.ForeignKey(Session_log)
	email_thread = models.ForeignKey(EmailThread)
	question = models.ForeignKey(Questions)
	knowledge_source = models.ForeignKey(KnowledgeSource)


class Click_log(models.Model):
	user = models.ForeignKey(User)
	session = models.ForeignKey(Session_log)
	timestamp_clicked = models.DateTimeField(default=timezone.now)
	SHOW_ACTION = '_show'
    	HIDE_ACTION = '_hide'
	ACTION_CHOICES = (
		(SHOW_ACTION, '_show'),
		(HIDE_ACTION,'_hide'),
	)
	click_action = models.CharField(choices = ACTION_CHOICES, default = SHOW_ACTION ,max_length=255)





        


	
	
