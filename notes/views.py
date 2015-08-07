from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
import json
from utils.decorators import inject_num_invites
from utils.conversions import load_json
from utils.utils import json_error_response, json_success_response
from tokenapi.decorators import token_required

from . import models

# Create your views here.
def test_view(request):
    return JsonResponse({'test':'super_test!'})

@csrf_exempt
@token_required
@inject_num_invites
def list_notes(request):
    '''A simple view that only response to ajax GET requests. Assuming the user can authenticate it will return a list of note titles and relevant dates.'''

    if request.method == 'GET':
        user = request.user
        if user is not None and user.is_active:
            notes = []
            for note in user.note_set.all(): #models.Note.objects.filter(owner=user):
                notes.append({'note_id': note.id,
                              'title': note.title,
                              'creation_date': note.creation_date_time,
                              'last_edit_date': note.last_edit_date_time
                })
                
            return json_success_response({'notes': notes})
        else:
            return json_error_response('Unknown user or incorrect password.')
            
    return HttpResponseBadRequest('Not a GET request.')
        
@csrf_exempt
@token_required
@inject_num_invites
def single_note(request):
    '''A view that lets a user access a single note in it's entirety (READ ONLY)'''
    if request.method == 'POST':
        user = request.user
        payload = load_json(request)
        
        note = None
        try:
            note = user.note_set.get(id=payload['note_id']) #models.Note.objects.filter(owner=user.id).get(id=payload['note_id'])
        except ObjectDoesNotExist:
            return json_error_response('Unknown note id for this user')

        data_points = []
        for point in note.data_points.all():
            
            data_points.append({'datum': point.datum,
                                'is_factual': point.is_factual,
                                'data_point_id': point.id,
                                'tags': list(map(lambda t: {'tag': t.tag}, point.tag_set.all()))
            })  
        return json_success_response({'title': note.title, # Does this need the id returned? Front end should be able to cache that
                                      'note_id': note.id,
                                      'summary': note.summary,
                                      'data_points': data_points,
                                      'queries': list(map(lambda q: q.query, note.searchquery_set.all())),
                                      'tags': list(map(lambda t: {'tag': t.tag}, note.tag_set.all()))
        })                       
            
    return HttpResponseBadRequest('Not an ajax call or not a GET request')

@csrf_exempt
@token_required
@inject_num_invites
def update_single_note(request):
    '''Allows posting of new or updated notes, or deleting a single note'''
    user = request.user
    if request.method == 'POST':
        payload = load_json(request)
        try:
            note = None
            if payload['is_new_note']:
                note = models.Note.create(title=payload['title'], summary=payload['summary'], private=True, owner=user)
                note.save()
            else:
                try:
                    note = user.note_set.get(id=payload['note_id']) #models.Note.objects.filter(owner=user.id).get(id=payload['note_id'])
                    note.summary = payload['summary']
                    note.title = payload['title']
                    note.save()
                except ObjectDoesNotExist:
                    return json_error_response('Unknown note_id for this user')
            data_points = payload['data_points']
            queries     = payload['queries']
            tags        = payload['tags']

            update_tags(note, tags)
            
            
            for query_entity in queries:
                note.searchquery_set.create(query=query_entity['query']).save()
                # Avoids resaving existing datapoints
            read_only_points = (models.DataPoint.objects.filter(private=False) | \
                                models.DataPoint.objects.filter(reviewers__id=user.id)).exclude(owner=user.id)
            for data_point in data_points:
                try:
                    data_point_id = data_point['data_point_id']
                    query_set = read_only_points.filter(id=data_point_id) 
                    if query_set.exists(): # add an existing, read only data point to a note (NO EDITING)
                        note.data_points.add(query_set.get(id=data_point_id))
                    else:
                        pt_to_edit = note.data_points.get(id=data_point_id)
                        pt_to_edit.datum = data_point['datum'] # Could throw a KeyError
                        pt_to_edit.save()
                        update_tags(pt_to_edit, data_point['tags'])
                except (ObjectDoesNotExist, KeyError): # Make a new note if it could not be found
                    new_data_point = note.data_points.create(datum=data_point['datum'], is_factual=False, private=True, owner=user)
                    update_tags(new_data_point, data_point['tags'])
            return json_success_response({}) 
        except KeyError:
            return json_error_response('Malformed JSON in note update request')
    elif request.method == 'DELETE': 
        payload = load_json(request)
        note_id = None
        try:
            note_id = payload['note_id']
        except KeyError:
            return json_error_response("Malformed JSON in note delete request")
        try:
            note = user.note_set.get(id=note_id)
            note.delete()
            return json_success_response({})
        except ObjectDoesNotExist:
            return json_error_response('Unknown user or incorrect note_id')
        
    return HttpResponseBadRequest('Not an ajax call or not a POST request')

@csrf_exempt
@token_required
@inject_num_invites
def find_similar(request):
    '''Finds similar notes, datapoints and sources for whatever note is provided'''
    if request.method == 'POST':
        user = request.user
        try:
            payload = load_json(request)
            note_id = payload['note_id']
            note = user.note_set.get(id=note_id) 
        except KeyError:
            return json_error_response('Malformed json in find_similar request')
        except ObjectDoesNotExist:
            return json_error_response('Unknown note_id for this user')
        note.add_similar_notes()
        for data_point in note.data_points.all():
            data_point.add_similar_data_points()
            
        # Need to add source.find_similar here whenever a) sources are used and b) the method is created
        try: # buildup return results
            similar_notes = []
            similar_data_points = []
            if payload['return_similar_notes']:
                for note in note.similar_notes.all():
                    similar_notes.append({
                        'note_id': note.id,
                        'title': note.title,
                    })
            if payload['return_similar_data_points']:
                for data_point in note.data_points.all():
                    for sim_pt in data_point.similar_data_points.all():
                        similar_data_points.append({
                            'data_point_id': sim_pt.id,
                            'datum': sim_pt.datum,
                            'is_factual': sim_pt.is_factual
                        })
            return json_success_response({
                'similar_notes' : similar_notes,
                'similar_data_points': similar_data_points
                })        
        except KeyError:
            return json_error_response('Found similar notes, BUT not sure if similar_notes or similar_data_points are needed (none returned)')
                
    return HttpResponseBadRequest('Not an ajax request or not a POST request')

def update_tags(model, tags):
    ''' Adds new tags to the model AND removes tags from the model that are 
    not in the tags list '''

    cleaned_tags = map(lambda tag_entity: tag_entity['tag'].lower(), tags)
    # Add new tags
    for tag in cleaned_tags:
        if not model.tag_set.filter(tag=tag).exists():
            if models.Tag.objects.filter(tag=tag).exists():
                found_tag = models.Tag.objects.get(tag=tag)
                model.tag_set.add(found_tag)
            else:
                model.tag_set.create(tag=tag)

    # Remove unneeded tags
    for tag_ref in model.tag_set.all():
        if tag_ref.tag not in cleaned_tags:
            model.tag_set.remove(tag_ref)
