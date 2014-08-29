from django.template import RequestContext
from django.shortcuts import render_to_response
from tango.models import Page

def index(request):
	# Obtain context from HTTP request.
	context = RequestContext(request)
	
	#Query for all categories. 
	page_list = Page.objects.order_by('-title')[:5]
	context_dict = {'pages': page_list}




	return render_to_response('tango/index.html', context_dict, context)
    
# Create your views here.
