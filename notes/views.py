from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def test_view(request):
    return JsonResponse({'test':'super_test!'})
