from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate
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


def list_notes(request):
    '''A simple view that only response to ajax GET requests. Assuming the user can authenticate it will return a list of note titles and relevant dates.''' 
    if request.is_ajax() and request.method == 'GET':
        payload = json.loads(request.raw_data)
        user = None
        try:            
            user = quick_authenticate(payload)                            
        except KeyError:
            return HttpResonseBadRequest("Username or password missing in request.")
        if user is not None and user.is_active:
            notes = []
            for note in models.Note.objects.filter(owner=user):
                notes.append({'note_id': note.id,
                               'title': note.title,
                               'creation_date': note.creation_date,
                               'last_edit_date': note.last_edit_date
                })
                
                return JsonResponse(notes)
            else:
                return HttpResponseBadRequest('Unknown user or incorrect password.')
            
    return HttpResponseBadRequest('Not an ajax call.')
        

def single_note(request):
    '''A view that lets a user access a single note in it's entirety (READ ONLY)'''
    if request.is_ajax() and request.method == 'GET':
        payload = json.loads(request.raw_data)
        user = None
        try:
            user = quick_authenticate(payload)
        except KeyError:
            return HttpResponseBadRequest('Malformed ajax request')
        
        note = None
        try:
            note = Note.objects.filter(owner=user.id).get(id=payload['note_id'])
        except DoesNotExist:
            return HttpResponseBadRequest('Unknown note id for this user')
        
        data_points = []
        for point in note.data_points.all():
            data_points.append({'datum': point.datum,
                                'is_factual': point.is_factual,
                                'data_point_id': point.id
            })                
        return JsonResponse({'title': note.title, # Does this need the id returned? Front end should be able to cache that
                             'summary': note.summary,
                             'data_points': data_points,
        })                       
            
    return HttpResponseBadRequest('Not an ajax call or not a GET request')

def update_single_note(request):
    '''Allows posting of new or updated notes'''
    if request.is_ajax() and request.method == 'POST':
        payload = json.loads(request.raw_data)
        user = None
        try:
            user = quick_authentication(payload)
            note = None
            if payload['is_new_note']:
                note = Note.create(title=payload['title'], summary=payload['summary'], private=True, owner=user)
                note.save()
            else:
                try:
                    note = Note.objects.filter(owner=user.id).get(id=payload['note_id'])
                except DoesNotExist:
                    return HttpResponseBadRequest('Unknown note_id for this user')
            for data_point in payload['data_points']:
                try: # Edit the datum on an existing note if it exists
                    pt_to_edit = note.data_points.get(data_point['data_point_id'])
                    pt_to_edit.datum = data_point['datum'] # Could throw a KeyError
                    pt_to_edit.save()
                except (DoesNotExist, KeyError): # Make a new note if it could not be found
                    note.data_points.create(datum=data_point['datum'], is_factual=False, private=True, owner=user)                
            return HttpResponse('Received POST') 
        except KeyError:
            return HttpResponseBadRequest('Malformed JSON in note update request')        
    return HttpResponseBadRequest('Not an ajax call or not a POST request')


def quick_authenticate(payload):
    return authenticate(username=payload['username'], password=payload['password'])
