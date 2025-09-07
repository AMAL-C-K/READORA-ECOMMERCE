from django.urls import path
from . import views
urlpatterns = [
    path('signup/',views.signUp,name='signup'),
    path('signin/',views.signIn,name='signin'),
    path('signout/',views.signOut, name='signout')
]