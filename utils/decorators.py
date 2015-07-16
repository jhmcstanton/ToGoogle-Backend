from django.http import JsonResponse, HttpResponse

class check_login_status(object):
    ''' This decorator checks if the user is logged in, and returns a failure JSON response if they are not'''
    def __init__(self):
        ...

    def __call__(self, view):
        def view_with_check(request):
            if request.user.is_authenticated():
                return view(request)
            else:
                return JsonResponse({'success': False, 'error': 'User is not logged in'})
        return view_with_check

class check_if_ajax(object):
    ''' Used to reduce boiler plate in API calls since most view (all at this time) will be ajax'''
    def __init__(self):
        ...

    def __call__(self, view):
        def view_with_ajax_check(request):
            if request.is_ajax():
                return view(request)
            else:
                return JsonResponse({'success': False, 'error': 'Expected ajax request'})
        return view_with_ajax_check

class allow_CORS(object):
    ''' Allows CORS for front end api '''
    def __init__(self):
        ...

    def __call__(self, view):
        def view_with_cors_headers(request):
            response = view(request)
            if response and isinstance(response, HttpResponse):
                response['Access-Control-Allow-Origin'] = '*'
                response['Access-Control-Max-Age'] = '120'
                response['Access-Control-Allow-Credentials'] = 'true'
                response['Access-Control-Allow-Methods'] = 'HEAD, GET, OPTIONS, POST, DELETE'
                response['Access-Control-Allow-Headers'] = 'origin, content-type, accept, x-requested-with'
            return response
        return view_with_cors_headers

class ajax_api_view(object):
    ''' Wraps a view with the check_login_status, check_if_ajax and allowCORS decorators for convenience'''
    def __init__(self):
        ...

    def __call__(self, view):
        @allow_CORS
        @check_if_ajax
        @check_login_status
        def wrapped_view(request):
            return view(request)
        return wrapped_view

