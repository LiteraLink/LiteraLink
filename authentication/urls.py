from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('show-profile/', views.show_profile, name='show_profile')
]