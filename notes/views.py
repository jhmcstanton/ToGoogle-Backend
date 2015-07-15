from django.shortcuts import render
from django.http import JsonResponse
from django.utils import simplejson

from . import models

# Create your views here.
def test_view(request):
    return JsonResponse({'test':'super_test!'})

def save_note(request):
    if request.is_ajax() and request.method == 'POST':
        note_load = simplejson.loads(request.raw_data)
        try:
            note = models.Note.create(note_load['title'], note_load['summary'])
            note.save()

            data_points = []
            for json_point in note_load['data_points']:
                point = models.DataPoint.create(json_point, False, False, note)
                point.save()
        except KeyError:
            return HttpResponseError("Malformed JSON Data")
        return HttpResponse("Received note, saved")
    return HttpResponseError("Incorrect request")


