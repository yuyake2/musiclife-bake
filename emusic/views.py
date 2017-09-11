# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse,HttpResponse


ERROR_MSG = {
    0: "ok.",
    1000: "Email Not Found.",
    1001: "Invalid Email Address.",
    1002: "Email already exists.",
    1003: 'Data : Invalid',
    1004: 'The username or password you entered is incorrect.',
    1005: 'This account not Found.',
    1006: 'This %s already exists.',
    
}
def home(request):
    return HttpResponse("Hello, world. You're at the polls index.")