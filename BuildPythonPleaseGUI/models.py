#python manage.py migrate --run-syncdb

from django.db import models
from django.contrib.auth.models import User, models

from django.db.models.signals import post_save
from django.dispatch import receiver

import uuid
def genid(prefix):

	return prefix+str(uuid.uuid4())

class Projects(models.Model):
	id = models.CharField(max_length=100,primary_key=True, default=genid("Project:"), editable=False)

	title = models.CharField(max_length=100)
	owner = models.CharField(max_length=75)
	version = models.CharField(max_length=15)
	client = models.CharField(max_length=75)
	description = models.TextField(max_length=100)
	status = models.CharField(max_length=15)
	payout = models.CharField(max_length=15)

#class Filter(models.Model):
#	search = models.CharField(max_length=75)

class Solution(models.Model):
	id = models.CharField(max_length=100,primary_key=True, default=genid("Solution:"), editable=False)

	project_id = models.CharField(max_length=100)
	solution = models.TextField()
	owner = models.CharField(max_length=75)
	sender = models.CharField(max_length=75)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.CharField(max_length=30, blank=True)
    is_admin = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

class Notifications(models.Model):
	username = models.CharField(max_length=75)
	link = models.CharField(max_length=75)
	title = models.CharField(max_length=75)
	is_new = models.BooleanField(default=True)