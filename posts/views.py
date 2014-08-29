from gab.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from posts.models import Conversation, Gab, CanPost, ListFriendToConversation, Friendship, Comment
import sys
import json as simplejson

def constructFriendRequests(friendrequests):
	friendrequests_end = {}
	for friend in friendrequests:
		sender = friend.sender
		full_name = sender.first_name + " " + sender.last_name
		profile = UserProfile.objects.get(user=sender)
		friendrequests_end[full_name] = profile.userid
	return friendrequests_end

def friend_accept(request, userid):
	context = RequestContext(request)
	current_user = request.user
	current_profile = UserProfile.objects.get(user=current_user)
	requester = UserProfile.objects.get(userid=userid)
	if request.method == 'POST':
		ship = Friendship.objects.get(sender=requester.user, sendee=current_user)
		ship.accepted = True
		ship.viewed = True
		ship.save()
		return HttpResponseRedirect('/profile/' + str(current_profile.userid))
	return HttpResponseRedirect('/profile/' + str(current_profile.userid))

def friend_request(request, userid):
	context = RequestContext(request)
	current_user = request.user
	current_profile = UserProfile.objects.get(user=current_user)
	requestee = UserProfile.objects.get(userid=userid)
	if request.method == 'POST':
		newship = Friendship(sender=current_user, sendee=requestee.user)
		newship.save()
		return HttpResponseRedirect('/profile/' + str(userid))
	return HttpResponseRedirect('/profile/' + str(userid))

def total_friends(friends_sent, friends_received):
	total = {}
	for friend in friends_sent:
		current = friend.sendee
		name = current.first_name + " " + current.last_name
		profile = UserProfile.objects.get(user=current)
		total[name] = profile.userid
	for friend in friends_received:
		current = friend.sender
		name = current.first_name + " " + current.last_name
		profile = UserProfile.objects.get(user=current)
		total[name] = profile.userid
	return total

def getFriends(current_user, numbertoretrieve):
	counter = 0
	potfriends = {}
	users = User.objects.all()
	for user in users:
		if user != current_user:
			filt = Friendship.objects.filter(sender=current_user, sendee=user)
			filt2 = Friendship.objects.filter(sender=user, sendee=current_user)
			if not filt:
				if not filt2:
					profile=UserProfile.objects.get(user=user)
					full_name = user.first_name + " " + user.last_name
					potfriends[full_name] = profile.userid
					counter = counter + 1
					if counter==numbertoretrieve:
						return potfriends
	return potfriends

@login_required(login_url='/login/')
def profile(request, profileid):
	context = RequestContext(request)
	current_user = request.user
	current_profile = UserProfile.objects.get(user=current_user)
	try:
		profile = UserProfile.objects.get(userid=profileid)
	except UserProfile.DoesNotExist:
		return HttpResponseRedirect('/')
	potentialusers = User.objects.all()
	potfriends = getFriends(current_user, 10)
	friendrequests = Friendship.objects.filter(sendee=current_user, accepted=False)
	friendrequests_end = constructFriendRequests(friendrequests)
	friends_sent = Friendship.objects.filter(sender=profile.user, accepted=True)
	friends_received = Friendship.objects.filter(sendee=profile.user, accepted=True)
	friends = total_friends(friends_sent, friends_received)
	friendnots = len(Friendship.objects.filter(sendee=current_user, accepted=False))
	return render_to_response('posts/profile.html', {'profile':profile, 'user': profile.user, 'current_user': current_user, 
		'current_profile':current_profile, 'potentialfriends': potfriends, 'friendrequests': friendrequests_end, 'friends': friends, 'friendnots': friendnots}, context)

def constructdict(conv):
	gabs = Gab.objects.filter(conversation=conv).order_by('posted_at')
	listgabs = []
	for gab in gabs:
		listgabs.append(gab)
	comments = Comment.objects.filter(conversation=conv).order_by('posted_at')
	listcomments = []
	for comment in comments:
		listcomments.append(comment)
	listconv = {}
	listconv['pk'] = conv.pk
	listconv['gabs'] = listgabs
	listconv['comm'] = listcomments
	return listconv

def getfeed(request, activelink):
	context = RequestContext(request)
	activelink = "friendly"
	current_user = request.user
	current_profile = UserProfile.objects.get(user=current_user)
	friends_sent = Friendship.objects.filter(sender=current_user, accepted=True)
	friends_received = Friendship.objects.filter(sendee=current_user, accepted=True)
	friends = total_friends(friends_sent, friends_received)
	conversations = Conversation.objects.all().order_by('-posted_at')
	stack = []
	for conv in conversations:
		convdict = constructdict(conv)
		stack.append(convdict)
		#print >>sys.stderr, convdict
	friendnots = len(Friendship.objects.filter(sendee=current_user, accepted=False))

	return render_to_response('posts/posts.html', {'current_user': current_user, 
		'current_profile': current_profile, 'stack': stack, 'friendnots': friendnots, 'friends': friends, 'activelink': activelink, }, context)


@login_required(login_url='login')
def posts(request):
	context = RequestContext(request)
	activelink = "friendly"
	current_user = request.user
	current_profile = UserProfile.objects.get(user=current_user)
	friends_sent = Friendship.objects.filter(sender=current_user, accepted=True)
	friends_received = Friendship.objects.filter(sendee=current_user, accepted=True)
	friends = total_friends(friends_sent, friends_received)
	conversations = Conversation.objects.all().order_by('-posted_at')
	stack = []
	for conv in conversations:
		convdict = constructdict(conv)
		stack.append(convdict)
		#print >>sys.stderr, convdict
	friendnots = len(Friendship.objects.filter(sendee=current_user, accepted=False))
	return render_to_response('posts/posts.html', {'current_user': current_user, 
		'current_profile': current_profile, 'stack': stack, 'friendnots': friendnots, 'friends': friends, 'activelink': activelink, }, context)

@login_required(login_url='login')
def pseudo_posts(request):
	context = RequestContext(request)
	activelink = "pseudo"
	current_user = request.user
	current_profile = UserProfile.objects.get(user=current_user)
	friends_sent = Friendship.objects.filter(sender=current_user, accepted=True)
	friends_received = Friendship.objects.filter(sendee=current_user, accepted=True)
	friends = total_friends(friends_sent, friends_received)
	conversations = Conversation.objects.filter(privacy='Pseudonym').order_by('-posted_at')
	stack = []
	for conv in conversations:
		convdict = constructdict(conv)
		stack.append(convdict)
		#print >>sys.stderr, convdict
	friendnots = len(Friendship.objects.filter(sendee=current_user, accepted=False))
	return render_to_response('posts/posts.html', {'current_user': current_user, 
		'current_profile': current_profile, 'stack': stack, 'friendnots': friendnots, 'friends': friends, 'activelink': activelink, }, context)


@login_required(login_url='login')
def private_posts(request):
	context = RequestContext(request)
	activelink = "private"
	current_user = request.user
	current_profile = UserProfile.objects.get(user=current_user)
	friends_sent = Friendship.objects.filter(sender=current_user, accepted=True)
	friends_received = Friendship.objects.filter(sendee=current_user, accepted=True)
	friends = total_friends(friends_sent, friends_received)
	conversations = Conversation.objects.filter(privacy='Private').order_by('-posted_at')
	stack = []
	for conv in conversations:
		convdict = constructdict(conv)
		stack.append(convdict)
		#print >>sys.stderr, convdict
	friendnots = len(Friendship.objects.filter(sendee=current_user, accepted=False))
	return render_to_response('posts/posts.html', {'current_user': current_user, 
		'current_profile': current_profile, 'stack': stack, 'friendnots': friendnots, 'friends': friends, 'activelink': activelink, }, context)


@login_required(login_url='login')
def friendly_posts(request):
	context = RequestContext(request)
	activelink = "friendly"
	current_user = request.user
	current_profile = UserProfile.objects.get(user=current_user)
	friends_sent = Friendship.objects.filter(sender=current_user, accepted=True)
	friends_received = Friendship.objects.filter(sendee=current_user, accepted=True)
	friends = total_friends(friends_sent, friends_received)
	conversations = Conversation.objects.filter(privacy='Friendly').order_by('-posted_at')
	stack = []
	for conv in conversations:
		convdict = constructdict(conv)
		stack.append(convdict)
		#print >>sys.stderr, convdict
	friendnots = len(Friendship.objects.filter(sendee=current_user, accepted=False))
	return render_to_response('posts/posts.html', {'current_user': current_user, 
		'current_profile': current_profile, 'stack': stack, 'friendnots': friendnots, 'friends': friends, 'activelink': activelink, }, context)

@login_required
def public_posts(request):
	context = RequestContext(request)
	activelink = 'public'
	current_user = request.user
	current_profile = UserProfile.objects.get(user=current_user)
	friends_sent = Friendship.objects.filter(sender=current_user, accepted=True)
	friends_received = Friendship.objects.filter(sendee=current_user, accepted=True)
	friends = total_friends(friends_sent, friends_received)
	conversations = Conversation.objects.filter(privacy='Public').order_by('-posted_at')
	stack = []
	for conv in conversations:
		convdict = constructdict(conv)
		stack.append(convdict)
		#print >>sys.stderr, convdict
	friendnots = len(Friendship.objects.filter(sendee=current_user, accepted=False))

	return render_to_response('posts/posts.html', {'current_user': current_user, 
		'current_profile': current_profile, 'stack': stack, 'friendnots': friendnots, 'friends': friends, 'activelink': activelink, }, context)

def change_bio(request):
	context = RequestContext(request)
	current_user = request.user
	current_profile = UserProfile.objects.get(user=current_user)
	if request.is_ajax():
		try:
			bio = request.POST['bio']
		except:
			return HttpResponse('Error')
		current_profile.bio = bio
		current_profile.save()	
		return HttpResponse(bio)
	elif request.method == 'POST':
		bio = request.POST['bio']
		current_profile.bio = bio
		current_profile.save()
	userid = current_profile.userid
	return HttpResponseRedirect('/profile/' + str(userid))

def parsetags(tags):
	parsed = tags.split('@')
	profiles = {}
	for name in parsed:
		if name != "":
			print >>sys.stderr, "name is " + name
			full_name = name.split(' ')
			user = User.objects.get(first_name=full_name[0], last_name=full_name[1])
			profile = UserProfile.objects.get(user=user)
			profiles[name] = profile
	return profiles

def gab_response(request, conversation):
	#print >>sys.stderr, "output"
	if request.method == 'GET':
		return HttpResponseRedirect('/posts/')
	current_user = request.user
	current_profile = UserProfile.objects.get(user=current_user)
	text = request.POST['gab']
	conv = Conversation.objects.get(pk=int(conversation))
	try:
		alreadyadded = CanPost.objects.get(conversation=conv, user=current_user)
		if not alreadyadded.test:
			comment = Comment(conversation=conv, text=text, user=current_user, profileid=current_profile.userid)
			comment.save()
			if request.is_ajax():
				data = {}
				data['profileid'] = current_profile.userid
				data['first_name'] = current_user.first_name
				data['last_name'] = current_user.last_name
				data['conversation'] = str(conv.pk)
				data['gab'] = text
				data['comment'] = "TRUE"
				return HttpResponse(simplejson.dumps(data), mimetype="application/json")
	except:
		pass
		comment = Comment(conversation=conv, text=text, user=current_user, profileid=current_profile.userid)
		comment.save()
		if request.is_ajax():
			data = {}
			data['profileid'] = current_profile.userid
			data['first_name'] = current_user.first_name
			data['last_name'] = current_user.last_name
			data['conversation'] = str(conv.pk)
			data['gab'] = text
			data['comment'] = "TRUE"
			return HttpResponse(simplejson.dumps(data), mimetype="application/json")
	gab = Gab(conversation=conv, text=text, user=current_user, profileid=current_profile.userid)
	gab.save()
	tags = request.POST['tag1']
	if tags != "":
		tagdict = parsetags(tags)
		for person, profile in tagdict.iteritems():
			try:
				added = CanPost.objects.get(conversation=conv, user=profile.user)
				if not added.test:
					canPost = CanPost(conversation=conv, user=profile.user, test=True)
					canPost.save()
					gab = Gab(conversation=conv, text=" was added.", user=profile.user, profileid=profile.userid)
					gab.save()
			except:
				pass
				canPost = CanPost(conversation=conv, user=profile.user, test=True)
				canPost.save()
				gab = Gab(conversation=conv, text=" was added.", user=profile.user, profileid=profile.userid)
				gab.save()
	if request.is_ajax():
		data = {}
		data['profileid'] = current_profile.userid
		data['first_name'] = current_user.first_name
		data['last_name'] = current_user.last_name
		data['conversation'] = str(conv.pk)
		data['gab'] = text
		return HttpResponse(simplejson.dumps(data), mimetype="application/json")
	return HttpResponseRedirect('/posts/')


def gab_post(request, visibility):
	#if request.is_ajax():
	#	return HttpResponse("testdata")

	if request.method == 'GET':
		return HttpResponseRedirect('/posts/')

	context = RequestContext(request)
	current_user = request.user
	current_profile = UserProfile.objects.get(user=current_user)

	if request.method == 'POST':
		text = request.POST['gab']
		user = current_user
		if visibility == 'public':
			conversation = Conversation(user=user, privacy='Public')
			conversation.save()
			gab = Gab(conversation=conversation, text=text, user=user, profileid=current_profile.userid)
			gab.save()
			canPost = CanPost(conversation=conversation, user=user, test=True)
			canPost.save()
			return HttpResponseRedirect('/public/')
		elif visibility == 'friendly':
			conversation = Conversation(user=user, privacy='Friendly')
			conversation.save()
			gab = Gab(conversation=conversation, text=text, user=user, profileid=current_profile.userid)
			gab.save()
			canPost = CanPost(conversation=conversation, user=user, test=True)
			canPost.save()
			return HttpResponseRedirect('/friendly/')
	return HttpResponseRedirect('/friendly/')

def public_face(request, userid):
	context = RequestContext(request)
	activelink = 'public'
	current_user = request.user
	if current_user.is_anonymous():
		conversations = Conversation.objects.filter(privacy='Public').order_by('-posted_at')
		stack = []
		for conv in conversations:
			convdict = constructdict(conv)
			stack.append(convdict)
		return render_to_response('posts/public_face.html', {'stack': stack,})
	current_profile = UserProfile.objects.get(user=current_user)
	friends_sent = Friendship.objects.filter(sender=current_user, accepted=True)
	friends_received = Friendship.objects.filter(sendee=current_user, accepted=True)
	friends = total_friends(friends_sent, friends_received)
	conversations = Conversation.objects.filter(privacy='Public').order_by('-posted_at')
	stack = []
	for conv in conversations:
		convdict = constructdict(conv)
		stack.append(convdict)
		#print >>sys.stderr, convdict
	friendnots = len(Friendship.objects.filter(sendee=current_user, accepted=False))

	return render_to_response('posts/public_face.html', {'current_user': current_user, 
		'current_profile': current_profile, 'stack': stack, 'friendnots': friendnots, 'friends': friends, 'activelink': activelink, }, context)



# Create your views here.
