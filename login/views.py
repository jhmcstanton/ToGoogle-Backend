from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from utils.conversions import load_json
from utils.utils import json_error_response, json_success_response

# Create your views here.

def ajax_login(request):
    if request.method == 'POST':
        payload = json.loads(request.raw_data)
        user = authenticate(username=payload['username'], password=payload['password'])
        if user is not None and user.is_active:
            login(request, user)
            return json_success_response({})
        else:
            return json_error_response('Unknown username or password, or user is inactive')
    return json_error_response('Not an ajax request or not a POST request')

def ajax_logout(request):
    logout(request)
    return json_success_response({})
        
