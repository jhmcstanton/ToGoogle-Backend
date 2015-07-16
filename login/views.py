from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import json

# Create your views here.

def ajax_login(request):
    if request.is_ajax() and request.method == 'POST':
        payload = json.loads(request.raw_data)
        user = authenticate(username=payload['username'], password=payload['password'])
        if user is not None and user.is_active:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Unknown username or password, or user is inactive'})
    return JsonResponse({'success': False, 'error': 'Not an ajax request or not a POST request'})

def ajax_logout(request):
    logout(request)
    return JsonResponse({'success': True})
        
