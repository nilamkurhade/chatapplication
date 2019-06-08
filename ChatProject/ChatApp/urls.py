from django.conf.urls import url
from ChatApp import views
from django.urls import path

# SET THE NAMESPACE!
app_name = 'ChatApp'
# Be careful setting the name to just /login use userlogin instead!
# Be careful setting the name to just /login use userlogin instead!
urlpatterns = [
    #url(r'^register/$', views.register, name='register'),
    url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^$', views.chatindex, name='chatIndex'),
    url(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
]