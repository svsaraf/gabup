from django.db import models

from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	activation_key = models.CharField(default="", max_length=40)
	key_expires = models.DateTimeField(default=0)
	verified = models.BooleanField(default=False)
	bio = models.TextField(default="")
	userid = models.IntegerField(default=0)

	def __unicode__(self):
		return self.user.username



# Create your models here.
