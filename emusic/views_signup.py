# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse, HttpResponse,JsonResponse
import re, urllib2, json
from emusic.user_services import MusicLifeSignupService
from emusic.views import ERROR_MSG
from emusic.models import Profile, MEMBER_GENDER
from django.contrib.auth import authenticate, login as django_login


@csrf_exempt
def signup(request):
        
    if request.method == "POST":
        data_parameter_dict = request.POST if request.method == 'POST' else request.GET
        try:
            fb_name = data_parameter_dict.get('fb_name', None)
            firstname =  data_parameter_dict.get('firstname', None)
            lastname = data_parameter_dict.get('lastname', None)
            email = data_parameter_dict.get('email', None)
            gender_str = data_parameter_dict.get('gender', None)
            fb_id = data_parameter_dict.get('fb_id', None)
            fb_image = data_parameter_dict.get('fb_image', None)
            fb_token = data_parameter_dict.get('fb_token', None)
            image_token = data_parameter_dict.get('oe', None)
            data = data_parameter_dict.get('data', {})
            force = data_parameter_dict.get('force', False)
        except:
            error_code = 1003
        
        if email is not None:
            email = urllib2.unquote(email).lower().strip()
        if gender_str is not None:
            gender = _get_gender(gender_str)
        if fb_image is not None:
            fb_image_str = "%s%s%s"%(fb_image,"&oe=",image_token)

        result = {}
        error_code = 0
        if email is None:
            result['error_code'] = 1000
            result['error_msg'] = ERROR_MSG[1000]
            if error_code == 0:
                error_code = 1000

        if error_code == 0:
            signup_facebook_service = MusicLifeSignupService()
            error_code,user, profile = signup_facebook_service.execute(request=request,
                                                                  firstname=firstname,
                                                                  lastname=lastname,
                                                                  email=email,
                                                                  gender=gender,
                                                                  fb_id=fb_id,
                                                                  fb_name=fb_name,
                                                                  fb_image=fb_image_str,
                                                                  fb_token=fb_token)

        if error_code == 0:
            result['email'] = profile.email
            result['firstname'] = profile.firstname
            result['lastname'] = profile.lastname
            result['fb_image'] = profile.get_data_json().get('fb_image', "")
            result['fb_token'] = profile.fb_token
            result['fb_id'] = profile.fb_id
            result['error_code'] = 0
    return HttpResponse(json.dumps(result, indent=2), content_type='application/json; charset=UTF-8')

def _get_gender(gender_str):
    for item in MEMBER_GENDER:
        if gender_str in item:
            gender = item[0]
    return gender





