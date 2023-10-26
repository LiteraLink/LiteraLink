from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'bibliofilia'

urlpatterns = [
    path('', views.showForum, name='showForum'),
    path('get-forum/', views.get_Forum_json, name='get_Forum_json'),
    path('create-forum-ajax/', views.add_Forum_ajax, name='add_Forum_ajax'),
    path('create-forum', views.create_Forum,name="create_Forum"),
    path('delete_Forum/<int:forum_id>/', views.delete_Forum, name='delete_Forum'),
    path('childforum.html', views.showChildForum, name='childforum'),
    path('showTest', views.showTest,name="showTest"),
]