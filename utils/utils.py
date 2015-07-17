from django.http import JsonResponse

def json_error_response(msg):
    return JsonResponse({'success': False, 'error': msg})

def json_success_response(base_dict):
    ''' Takes a dictionary of outgoing data and adds a success state of True, always overwrites 'success' key '''
    base_dict['success'] = True
    return JsonResponse(base_dict)
