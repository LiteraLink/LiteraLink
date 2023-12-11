from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'bibliofilia'

urlpatterns = [
    path('', views.showForum, name='showForum'),
    path('get_forum/', views.get_Forum_json, name='get_Forum_json'),
    path('get_ForumReply_json/', views.get_ForumReply_json, name='get_ForumReply_json'),
    path('add_Forum_ajax/', views.add_Forum_ajax, name='add_Forum_ajax'),
    path('add_replies_ajax', views.add_replies_ajax, name='add_replies_ajax'),
    path('create_forum', views.create_Forum,name="create_Forum"),
    path('delete_Forum/<int:forum_id>/', views.delete_Forum, name='delete_Forum'),
    path('delete_replies/<int:reply_id>/', views.delete_Replies, name='delete_Replies'),
    path('forum/<int:forum_id>/', views.showChildForum, name='showChildForum'),
    path('add_Forum_flutter/', views.add_Forum_flutter, name='add_Forum_flutter'), #for flutter
    path('add_replies_flutter/', views.add_replies_flutter, name='add_replies_flutter'), #for flutter
    path('delete_forum_flutter/', views.delete_Forum_Flutter, name='delete_Forum_Flutter'), #for flutter
    path('delete_replies_flutter/', views.delete_Replies_Flutter, name='delete_Replies_Flutter'), #for flutter
    path('get_ForumReply_flutter/<int:forum_id>/', views.get_ForumReply_json_flutter, name='get_ForumReply_json_flutter'), #for flutter
    path('get_ForumReplyHead_json_flutter/<int:forum_id>/', views.get_ForumReplyHead_json_flutter, name='get_ForumReplyHead_json_flutter'), #for flutter
]