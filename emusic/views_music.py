# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse, HttpResponse
from emusic.models import Music, MUSIC_STATUS
from emusic.music_services import MusicListService, FavoriteMusicService

import json


def get_music_list(request):
    result = {}
    error_code = 0

    music_service = MusicListService()
    error_code, music = music_service.execute(request=request)
    
    result = music
    return HttpResponse(json.dumps(result, indent=2), content_type='application/json; charset=UTF-8')


@csrf_exempt
def update_favorite(request):
    
    profile_id = request.GET.get('profile_id', None)
    music_id = request.GET.get('music_id', None)
    is_active = request.GET.get('is_active', False)

    favorite_music = FavoriteMusicService()
    error_code, favorite = favorite_music.execute(request=request,
                                                  profile_id=profile_id,
                                                  music_id=music_id,
                                                  is_active=is_active)