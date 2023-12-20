from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('show-profile/', views.show_profile, name='show_profile'),
    path('signup-flutter/', views.signup_flutter, name='signup_flutter'),
    path('signin-flutter/', views.signin_flutter, name='signin_flutter'),
    path('signout-flutter/', views.signout_flutter, name='signout_flutter'),
    path('show-all-profile/', views.show_all_profile, name='show_all_profile'),
    path('get-history/<str:username>/', views.show_history, name='show_history'),
]