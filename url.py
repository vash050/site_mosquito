from datetime import date

from views import IndexView, AboutView, NotFound404View


def secret_front(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

routes = {
    '/': IndexView(),
    '/about/': AboutView(),
}
