from gab.forms import UserForm, UserProfileForm
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from gab.models import UserProfile
import random
import sha
import datetime
from django.core.mail import send_mail
from djangoappengine.utils import on_production_server
import sys
from django.core.urlresolvers import reverse


def verify(request, key):
	context = RequestContext(request)
	try:
		profile = UserProfile.objects.get(activation_key = key)
	except UserProfile.DoesNotExist:
		return render_to_response('gab/login.html', {'alert_message': "Verification failed!"}, context)
	if datetime.datetime.now() < profile.key_expires:
		profile.verified = True
		profile.save()
		return render_to_response('gab/login.html', {'alert_message': "Verification worked! Go ahead and log in!"}, context)
	return render_to_response('gab/login.html', {'alert_message': "Verification failed!"}, context)

def send_verification_email(first_name, email_account, activation_key):
	email_subject = "Gabup Verification Email!"
	email_body = "Hello %s! Thanks for trying out the alpha version of gabup!\n\nTo activate your account, click this link: \
	\n\nhttp://www.gabup.com/verify/%s \n\n Let us know if you need anything else! \n\n -sanjay" % (first_name, activation_key)
	if on_production_server:
		send_mail(email_subject, email_body, 'info@snake-mercury.appspotmail.com', [email_account])
	else:
		output = email_body + " sent to " + email_account
		print >>sys.stderr, output
	return True

def user_logout(request):
	logout(request)
	try:
		link = request.GET['next']
		return HttpResponseRedirect(link)
	except:
		pass
	return HttpResponseRedirect('/')

def user_login(request):
	context = RequestContext(request)

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)

		if user is not None:
			if user.is_active:
				profile = UserProfile.objects.get(user=user)
				if profile.verified:
					login(request, user)
					login_message = ""
					return HttpResponseRedirect(reverse('friendly_posts'))
				else:
					logout(request)
					login_message = "Profile is not verified! Check your email!"
					return render_to_response('gab/login.html', {'alert_message': login_message}, context)
			else:
				return render_to_response('gab/login.html', {'alert_message': "Your account is disabled"}, context)
		else:
			return render_to_response('gab/login.html', {'alert_message': "Invalid login details."}, context)
	else: 
		#user_form = UserForm()
		#profile_form = UserProfileForm()
		return render_to_response('gab/login.html', {}, context)

def register(request):
	context = RequestContext(request)
	if request.user.is_authenticated():
		profile = UserProfile.objects.get(user=request.user)
		return HttpResponseRedirect('/friendly/')
	registered = False

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.username = user.email
			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit=False)
			profile.user = user
			if len(UserProfile.objects.all()) > 0:
				mostrecentuser = UserProfile.objects.all().order_by('-userid')[0]
				profile.userid = mostrecentuser.userid+1
			else:
				profile.userid = 1
			salt = sha.new(str(random.random())).hexdigest()[:5]
			profile.activation_key = sha.new(salt+user.email).hexdigest()
			profile.key_expires = datetime.datetime.today() + datetime.timedelta(days=2)
			profile.bio="Newbie"
			profile.save()

			send_verification_email(user.first_name, user.email, profile.activation_key)

			registered = True

			return render_to_response('gab/verification.html',
				{'registered':registered}, context)
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render_to_response(
			'gab/register.html',
			{'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
			context)
