# -*- coding: utf-8 -*-
from django.conf.urls import url
from emusic import views, views_signup, views_music

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^api/signup/', views_signup.signup),
    # url(r'^api/login/', views_signup.login),
    url(r'^api/music/list/', views_music.get_music_list, name="api_music_list"),
    url(r'^api/update/favorite/', views_music.update_favorite, name="api_update_favorite"),
]

