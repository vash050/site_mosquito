from mosquito_framework.main import Mosquito
from url import routes, fronts
from wsgiref.simple_server import make_server


application = Mosquito(routes, fronts)

with make_server('', 8080, application) as httpd:
    print('Serving on port 8080...')
    httpd.serve_forever()
