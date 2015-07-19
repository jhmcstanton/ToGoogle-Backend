from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
import json
from utils.decorators import allow_CORS, ajax_api_view
from utils.conversions import load_json
from utils.utils import json_error_response, json_success_response

from . import models

# Create your views here.
def test_view(request):
    return JsonResponse({'test':'super_test!'})

@csrf_exempt
@allow_CORS()
def handle_note(request): # Not currently in use, and not necessary any more
    if request.is_ajax():
        note_load = load_json(request)
        if request.method == 'POST':            
            try:
                note = models.Note.create(note_load['title'], note_load['summary'])
                note.save()
                
                data_points = []
                for json_point in note_load['data_points']:
                    point = models.DataPoint.create(json_point, False, False, note)
                    point.save()
            except KeyError:
                return json_error_response("Malformed JSON Data in POST Request")
            return json_success_resposne({})
        elif request.method == 'GET':
            try:
                note = models.Note.objects.get(pk=note_load['note_key'])
                data_points = []
                for point in note.data_points.all():
                    data_points.append(point.datum)
                    
                return json_success_response({
                    'title': note.title,                    
                    'summary': note.summary,
                    'data_points': data_points,
                })
            
            except KeyError:
                return json_error_response('Malformed JSON data in GET request')
        else:
            #return HttpResponseBadRequest("Incorrect method in request.")
            return json_error_response('Incorrect method in request, expected GET')
        
    return HttpResponseBadRequest("Incorrect request")

@csrf_exempt
@allow_CORS()
def list_notes(request):
    '''A simple view that only response to ajax GET requests. Assuming the user can authenticate it will return a list of note titles and relevant dates.''' 
    if request.method == 'POST':
        payload = load_json(request) #json.loads(request.body.decode('utf-8'))
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
                               'creation_date': note.creation_date_time,
                               'last_edit_date': note.last_edit_date_time
                })
                
            return json_success_response({'notes': notes })
        else:
            return json_error_response('Unknown user or incorrect password.')
            
    return HttpResponseBadRequest('Not POST or Not an ajax call.')
        
@csrf_exempt
@allow_CORS()
def single_note(request):
    '''A view that lets a user access a single note in it's entirety (READ ONLY)'''
    if request.method == 'POST':
        payload = load_json(request)
        user = None
        try:
            user = quick_authenticate(payload)
        except KeyError:
            return json_error_response('Malformed ajax request')
        
        note = None
        try:
            note = models.Note.objects.filter(owner=user.id).get(id=payload['note_id'])
        except ObjectDoesNotExist:
            return json_error_response('Unknown note id for this user')

        data_points = []
        for point in note.data_points.all():
            
            data_points.append({'datum': point.datum,
                                'is_factual': point.is_factual,
                                'data_point_id': point.id,
                                'tags': list(map(lambda t: t.tag, point.tag_set.all()))
            })  
        return json_success_response({'title': note.title, # Does this need the id returned? Front end should be able to cache that
                                      'note_id': note.id,
                                      'summary': note.summary,
                                      'data_points': data_points,
                                      'tags': list(map(lambda t: t.tag, note.tag_set.all()))
        })                       
            
    return HttpResponseBadRequest('Not an ajax call or not a GET request')

@csrf_exempt
@allow_CORS()
def update_single_note(request):
    '''Allows posting of new or updated notes, or deleting a single note'''
    user = None
    if request.method == 'POST':
        payload = load_json(request)
        try:
            user = quick_authenticate(payload)
            note = None
            if payload['is_new_note']:
                note = models.Note.create(title=payload['title'], summary=payload['summary'], private=True, owner=user)
                note.save()
            else:
                try:
                    note = models.Note.objects.filter(owner=user.id).get(id=payload['note_id'])
                except ObjectDoesNotExist:
                    return json_error_response('Unknown note_id for this user')
            data_points = payload['data_points']
            read_only_points = (models.DataPoint.objects.filter(private=False) | \
                                models.DataPoint.objects.filter(reviewers__id=user.id)).exclude(owner=user.id)
            for data_point in data_points:
                try:
                    data_point_id = data_point['data_point_id']
                    query_set = read_only_points.filter(id=data_point_id) 
                    if query_set.exists(): # add an existing, read only data point to a note (NO EDITING)
                        note.data_points.add(query_set.get(id=data_point_id))
                        note.save()
                    else:
                        pt_to_edit = note.data_points.get(id=data_point['data_point_id'])
                        pt_to_edit.datum = data_point['datum'] # Could throw a KeyError
                        pt_to_edit.save()
                except (ObjectDoesNotExist, KeyError): # Make a new note if it could not be found
                    note.data_points.create(datum=data_point['datum'], is_factual=False, private=True, owner=user)
            return json_success_response({}) 
        except KeyError:
            return json_error_response('Malformed JSON in note update request')
    elif request.method == 'DELETE': 
        payload = load_json(request)
        user = None
        note_id = None
        try:
            user = quick_authenticate(payload)
            note_id = payload['note_id']
        except KeyError:
            return json_error_response("Malformed JSON in note delete request")
        try:
            models.Note.objects.filter(owner=user).get(id=note_id).delete()
            return json_success_response({})
        except ObjectDoesNotExist:
            return json_error_response('Unknown user or incorrect note_id')
        
    return HttpResponseBadRequest('Not an ajax call or not a POST request')


def quick_authenticate(payload):
    return authenticate(username=payload['username'], password=payload['password'])
