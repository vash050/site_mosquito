import copy
import quopri

from patterns.architectural_system_pattern_unit_of_work import DomainObject
from patterns.behavioral_patterns import ConsoleWriter, Subject, EmailNotifier, SmsNotifier

email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()
subject = Subject()


class User:
    def __init__(self, name=None):
        self.name = name


class Teacher(User):
    pass


class Student(User, DomainObject):
    pass


# паттерн фабричный метод
class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher
    }

    # паттерн фабричный метод
    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


# паттерн прототип
class CoursePrototype:

    def clone(self):
        return copy.deepcopy(self)


class Course(CoursePrototype):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []

    def add_student(self, student):
        self.students.append(student)
        subject.observers.append(student)
        subject.notify()
        # email_notifier.update(self.students)
        # sms_notifier.update(self.students)


class WebinarCourse(Course):
    pass


class OfflineCourse(Course):
    pass


class Category:
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


# паттерн фабричный метод
class CourseFactory:
    types = {
        'webinar': WebinarCourse,
        'offline': OfflineCourse
    }

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


class Engine:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type_, name):
        print(type_, name)
        return UserFactory.create(type_, name)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for el in self.categories:
            print('el', el.id)
            if el.id == id:
                return el
        raise Exception(f'Нет категории с id = {id}')

    @staticmethod
    def create_course(type_, name, category):
        return CourseFactory.create(type_, name, category)

    def get_course(self, name):
        for el in self.courses:
            if el.name == name:
                return el
        return None

    def get_student(self, name):
        for el in self.students:
            if el.name == name:
                return el

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace('+', ''), 'UTF-8')
        val_decode_str = quopri.decodestring(val_b)
        return val_decode_str.decode('UTF-8')


# паттерн синглон
class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name, writer=ConsoleWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        text = f'log---> {text}'
        self.writer.write(text)
