from mosquito_framework.templator import render


class IndexView:
    def __call__(self, request):
        return '200 OK', render('index.html', data=request.get('data', None))


class AboutView:
    def __call__(self, request):
        return '200 OK', render('contact.html')


class NotFound404View:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'

