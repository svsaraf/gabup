# when making changes to these models be sure to dumpdata and loaddata:
# python manage.py dumpdata --indent=4 --exclude=auth > shipping.json
# python manage.py syncdb
# python manage.py loaddata doesn't work because I can't save the auth users...yet. 

#Alternatively, you can drop the tables from /_ah/admin and then just use python manage.py syncdb. :)	

from django.db import models

from django.contrib.auth.models import User

class Conversation(models.Model):
	OPTIONS = (
		('PU', 'Public'),
		('FR', 'Friendly'),
		('PR', 'Private'),
		('PS', 'Pseudo'),
	)
	user = models.ForeignKey(User)
	posted_at = models.DateTimeField(auto_now_add=True)
	privacy = models.CharField(max_length=2, choices=OPTIONS, default='Friendly')
	title = models.CharField(max_length=150, default="")
	# slug -> public
	# class -> public/friendly/private/pseudo
	# pseudonym -> pseudo
	# title -> public
# class Comment -> public, friendly	

	def __unicode__(self):
		return self.user.username + " posted at " + self.posted_at.strftime('%m/%d/%Y')

class Gab(models.Model):
	conversation = models.ForeignKey(Conversation)
	posted_at = models.DateTimeField(auto_now_add=True)
	text = models.TextField(default="", max_length=10000) # changed retroactively. 
	user = models.ForeignKey(User)
	profileid = models.IntegerField(default=0)

	def __unicode__(self):
		return self.user.username + " posted " + self.text[:100] + " at " + self.posted_at.strftime('%m/%d/%Y')

class Comment(models.Model):
	conversation = models.ForeignKey(Conversation)
	posted_at = models.DateTimeField(auto_now_add=True)
	text = models.TextField(default="", max_length=10000)
	user = models.ForeignKey(User)
	profileid = models.IntegerField(default=0)

	def __unicode__(self):
		return self.user.username + " commented " + self.text[:100] + " at " + self.posted_at.strftime('%m/%d/%Y')

class CanPost(models.Model):
	conversation = models.ForeignKey(Conversation)
	user = models.ForeignKey(User)
	test = models.BooleanField(default=False)

	def __unicode__(self):
		return self.user.username + " can post in " + str(self.test)

class ListFriendToConversation(models.Model):
	conversation = models.ForeignKey(Conversation)
	friend = models.ForeignKey(User)
	posted_at = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.friend.username + " can see " + self.conversation

class Friendship(models.Model):
	sender = models.ForeignKey(User, related_name='friendship_senders')
	sendee = models.ForeignKey(User, related_name='friendship_sendees')
	accepted = models.BooleanField(default=False)
	viewed = models.BooleanField(default=False)

class PublicLink(models.Model):
	user = models.ForeignKey(User)
	conversation = models.ForeignKey(Conversation)
	slug = models.SlugField()
	title = models.CharField(max_length=200)
	posted_at = models.DateTimeField(auto_now_add=True)

class PseudoLink(models.Model):
	user = models.ForeignKey(User)
	posted_at = models.DateTimeField(auto_now_add=True)
	displayname = models.CharField(max_length=100)
	title = models.CharField(max_length=200)
	slug = models.SlugField()



# Create your models here.
