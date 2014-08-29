from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from posts.models import Conversation, Gab, CanPost, ListFriendToConversation, Friendship, Comment
from gab.models import UserProfile


# Create your views here.
def local_news(request):
	context = RequestContext(request)
	current_user = request.user
	current_profile = UserProfile.objects.get(user=current_user)
	stack = Conversation.objects.all().exclude(title="")
	return render_to_response('news/feed.html', {'profile':current_profile, 'user': current_profile.user, 'current_user': current_user, 
		'current_profile':current_profile, 'posts':stack, }, context)
