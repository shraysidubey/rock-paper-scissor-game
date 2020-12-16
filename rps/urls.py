from django.conf.urls import patterns, url
from rps import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^play_games/(?P<user_choice>[\w\-]+)/$', views.play_game, name='play_game'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
)