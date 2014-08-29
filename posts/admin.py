from django.contrib import admin
from posts.models import Conversation, Gab, CanPost, ListFriendToConversation, Comment, Friendship

admin.site.register(Conversation)
admin.site.register(Gab)
admin.site.register(CanPost)
admin.site.register(ListFriendToConversation)
admin.site.register(Comment)
admin.site.register(Friendship)

