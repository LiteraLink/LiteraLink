from django.contrib import admin
from .models import Forum
from .models import ForumReply

class ForumAdmin(admin.ModelAdmin):
    list_display = ('BookName', 'user', 'dateOfPosting', 'repliesTotal')
    search_fields = ('BookName', 'user__username', 'forumsDescription')
    list_filter = ('dateOfPosting', 'user')
    list_per_page = 20  # Number of items displayed per page in the admin list

admin.site.register(Forum, ForumAdmin)



class ForumReplyAdmin(admin.ModelAdmin):
    list_display = ('forum', 'user', 'timestamp')
    search_fields = ('forum__BookName', 'user__username', 'text')
    list_filter = ('timestamp', 'user')
    list_per_page = 20

admin.site.register(ForumReply, ForumReplyAdmin)