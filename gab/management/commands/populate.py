from django.core.management.base import BaseCommand
from gab.models import UserProfile
from django.contrib.auth.models import User
'''
from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from gab.models import UserProfile 
from django.contrib.auth.models import User
import string
import sys
'''
class Command(BaseCommand):
	args = '<foo bar ...>'
	help = 'our help string goes here'

	def _createProfiles(self):
		person = 'test_john@email.com'
		verified = True
		first_name = person[:4]
		location = string.find(person, '@')
		last_name = person[5:location]
		password = 'testpass'
		p, c = User.objects.get_or_create(username=person, email=person, first_name=first_name, last_name=last_name, password=password)
		p.save()
		self.stdout.write("HELLO!")
		salt = sha.new(str(random.random())).hexdigest()[:5]
		p_activation_key = sha.new(salt+user.email).hexdigest()
		p_key_expires = datetime.datetime.today() + datetime.timedelta(days=2)
		profile = UserProfile.objects.get_or_create(user=p, activation_key=p_activation_key, key_expires=p_key_expires)
		if verified:
			profile.verified = True
		profile.save()

	def handle(self, *args, **options):
		self._createProfiles
'''
	def add_User_and_Profile(person, verified):
	    first_name = person[:4]
	    location = string.find(person, '@')
	    last_name = person[5:location]
	    password = 'testpass'
	    p, c = User.objects.get_or_create(username=person, email=person, first_name=first_name, last_name=last_name, password=password)
	    p.save()

	    salt = sha.new(str(random.random())).hexdigest()[:5]
	    p_activation_key = sha.new(salt+user.email).hexdigest()
	    p_key_expires = datetime.datetime.today() + datetime.timedelta(days=2)
	    profile = UserProfile.objects.get_or_create(user=p, activation_key=p_activation_key, key_expires=p_key_expires)
	    if verified:
	        profile.verified = True
	    profile.save()
	    return p

	def handle(self, *args, **options):
		hello = ['test_john@email.com', 'test_jack@email.com', 'test_jim@email.com', 'test_joan@email.com']
		verified_users = ['test_bill@email.com,', 'test_bob@email.com', 'test_bjorn@email.com', 'test_bart@email.com']
    	self.stdout.write(hello)
    	for person in unverified_users:
       		add_User_and_Profile(person, False)
    	for person in verified_users:
        	add_User_and_Profile(person, True)
'''