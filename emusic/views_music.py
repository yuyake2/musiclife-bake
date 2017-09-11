# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse, HttpResponse
from emusic.models import Music, MUSIC_STATUS
from emusic.music_services import MusicListService

import json


def get_music_list(request):
    result = {}
    error_code = 0

    music_service = MusicListService()
    error_code, music = music_service.execute(request=request)
    
    result = music
    return HttpResponse(json.dumps(result, indent=2), content_type='application/json; charset=UTF-8')
        