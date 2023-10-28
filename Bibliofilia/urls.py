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
    path('showTest', views.showTest,name="showTest"),
]