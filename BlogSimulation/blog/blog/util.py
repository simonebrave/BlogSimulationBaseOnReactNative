import json
from web import EmulateWeb

def jsonify(status=200, **kwargs):
    content = json.dumps(kwargs)
    response = EmulateWeb.Response()
    response.status_code = status
    response.content_type = 'application/json'
    response.charset = 'utf-8'
    response.body = '{}'.format(content).encode()

    return response


