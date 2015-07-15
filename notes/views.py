from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
import json

from . import models

# Create your views here.
def test_view(request):
    return JsonResponse({'test':'super_test!'})

def handle_note(request):
    if request.is_ajax():
        note_load = json.loads(request.raw_data)
        if request.method == 'POST':            
            try:
                note = models.Note.create(note_load['title'], note_load['summary'])
                note.save()
                
                data_points = []
                for json_point in note_load['data_points']:
                    point = models.DataPoint.create(json_point, False, False, note)
                    point.save()
            except KeyError:
                return HttpResponseBadRequest("Malformed JSON Data in POST request")
            return HttpResponse("Received note, saved")
        elif request.method == 'GET':
            try:
                note = models.Note.objects.get(pk=note_load['note_key'])
                data_points = []
                for point in note.data_points.all():
                    data_points.append(point.datum)
                    
                return JsonResponse({'title': note.title,
                                     'summary': note.summary,
                                     'data_points': data_points,
                                     })
            except KeyError:
                return HttpResponseBadRequest("Malformed JSON Data in GET request")
        else:
            return HttpResponseBadRequest("Unexpected AJAX request")
            
    return HttpResponseBadRequest("Incorrect request")

