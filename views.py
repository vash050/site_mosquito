from mosquito_framework.templator import render


class IndexView:
    def __call__(self, request):
        output = render('index.html')
        return '200 OK', [bytes(output, encoding='utf-8')]


class AboutView:
    def __call__(self, request):
        print(request)
        output = render('contact.html')
        return '200 OK', [bytes(output, encoding='utf-8')]


class NotFoundPage404View:
    def __call__(self, request):
        print(request)
        return '404 ERROR', [b'404 PAGE NOT FOUND']


class Other:
    def __call__(self, request):
        print(request)
        return '200 OK', [b'<h1>other</h1>']