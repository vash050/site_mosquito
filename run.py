from mosquito_framework.main import Mosquito, DebugApplication, FakeApplication
from url import fronts
from wsgiref.simple_server import make_server

from views import routes

application = Mosquito(routes, fronts)
# application = DebugApplication(routes, fronts)
# application = FakeApplication(routes, fronts)

with make_server('', 8080, application) as httpd:
    print('Serving on port 8080...')
    httpd.serve_forever()
