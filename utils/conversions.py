import json

def load_json(request):
    return json.loads(request.body.decode('utf-8'))
