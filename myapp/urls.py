from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'gab.views.register', name='index'),
    # url(r'^myapp/', include('myapp.foo.urls')),
    url(r'^tango/', include('tango.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^register/', 'gab.views.register', name='register'),
    url(r'^login/', 'gab.views.user_login', name='login'),
    url(r'^logout/', 'gab.views.user_logout', name='logout'),
    url(r'^verify/(?P<key>[\w]+)/$', 'gab.views.verify', name='verify'), 
    

    url(r'^profile/(?P<profileid>[0-9]+)/$', 'posts.views.profile', name='profile'),
    url(r'^posts/', 'posts.views.posts', name='posts'),
    url(r'^gab_post/(?P<visibility>[a-zA-Z]+)/$', 'posts.views.gab_post', name='gab_post'),
    url(r'^change_bio/', 'posts.views.change_bio', name='change_bio'),
    url(r'^gab_response/(?P<conversation>[0-9]+)/$', 'posts.views.gab_response', name='gab_response'),
    url(r'^friends/request/(?P<userid>[0-9]+)/$', 'posts.views.friend_request', name='friend_request'),
    url(r'^friends/accept/(?P<userid>[0-9]+)/$', 'posts.views.friend_accept', name='friend_accept'),
    url(r'^public/$', 'posts.views.public_posts', name='public_posts'),
    url(r'^friendly/$', 'posts.views.friendly_posts', name='friendly_posts'),
    url(r'^private/$', 'posts.views.private_posts', name='private_posts'),
    url(r'^pseudo/$', 'posts.views.pseudo_posts', name='pseudo_posts'),
    url(r'^public/(?P<userid>[0-9]+)/$', 'posts.views.public_face', name='public_face'),

    url(r'^news/$', 'news.views.local_news', name='local_news'),
    
)
