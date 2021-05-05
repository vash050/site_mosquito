import jsonpickle

from mosquito_framework.templator import render


# паттерн наблюдатель
class Observer:
    def update(self, subject):
        pass


class Subject:
    def __init__(self):
        self.observers = []

    def notify(self):
        student = self.observers[-1]
        for el in self.observers:
            print(f'message to user {el.name}')
            sms = SmsNotifier()
            email = EmailNotifier()
            sms.update(subject=student)
            email.update(subject=student)


class SmsNotifier(Observer):
    def update(self, subject):
        print(('SMS ->', 'к нам присоединился', subject.name))


class EmailNotifier(Observer):
    def update(self, subject):
        print(('EMAIL ->', 'к нам присоединился', subject.name))


class BaseSerializer:
    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return jsonpickle.dumps(self.obj)

    @staticmethod
    def load(data):
        return jsonpickle.loads(data)


# Шаблонны метод
class TemplateView:
    template_name = 'template.html'

    def get_context_data(self):
        return {}

    def get_template(self):
        return self.template_name

    def render_template_with_context(self):
        template_name = self.get_template()
        context = self.get_context_data()
        return '200 OK', render(template_name, **context)

    def __call__(self, request):
        return self.render_template_with_context()


class ListView(TemplateView):
    queryset = []
    template_name = 'list.html'
    content_object_name = 'objects_list'

    def get_queryset(self):
        print(self.queryset)
        return self.queryset

    def get_context_object_name(self):
        return self.content_object_name

    def get_context_data(self):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context


class CreateView(TemplateView):
    template_name = 'create.html'

    @staticmethod
    def get_request_data(request):
        return request['data']

    def create_obj(self, data):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            data = self.get_request_data(request)
            self.create_obj(data)

            return self.render_template_with_context()
        else:
            return super().__call__(request)


# паттерн Стратегия
class ConsoleWriter:
    def write(self, text):
        print(text)


class FileWriter:
    def __init__(self, file_name):
        self.file_name = file_name

    def write(self, text):
        with open(self.file_name, 'a', encoding='utf-8') as f:
            f.write(f'{text}\n')
