from datetime import date

from mosquito_framework.templator import render
from patterns.architectul_system_patterns_mappers import MapperRegistry
from patterns.architectural_system_pattern_unit_of_work import UnitOfWork

from patterns.creational_patterns import Engine, Logger
from patterns.structural_patterns import AppRoute, Debug
from patterns.behavioral_patterns import EmailNotifier, SmsNotifier, BaseSerializer, ListView, CreateView

site = Engine()
logger = Logger('main')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry=MapperRegistry)

routes = {}


@AppRoute(routes=routes, url='/')
class IndexView:
    @Debug(name='IndexView')
    def __call__(self, request):
        return '200 OK', render('index.html', object_list=site.categories)


@AppRoute(routes=routes, url='/about/')
class AboutView:
    @Debug(name='AboutView')
    def __call__(self, request):
        return '200 OK', render('contact.html')


class NotFound404View:
    @Debug(name='NotFound404View')
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


@AppRoute(routes=routes, url='/study-programs/')
class StudyPrograms:
    @Debug(name='StudyPrograms')
    def __call__(self, request):
        return '200 OK', render('study-programs.html', data=date.today())


@AppRoute(routes=routes, url='/courses-list/')
class CoursesList:
    @Debug(name='CoursesList')
    def __call__(self, request):
        logger.log('список курсов')
        try:
            category = site.find_category_by_id(int(request['request_params']['id']))
            return '200 OK', render('course_list.html', object_list=category.courses, name=category.name,
                                    id=category.id)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


@AppRoute(routes=routes, url='/create-course/')
class CreateCourse:
    category_id = -1

    @Debug(name='CreateCourse')
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course('offline', name, category)
                # course.observers.append(email_notifier)
                # course.observers.append(sms_notifier)
                site.courses.append(course)

            return '200 OK', render('course_list.html', object_list=category.courses, name=category.name,
                                    id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_course.html', name=category.name, id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


@AppRoute(routes=routes, url='/create-category/')
class CreateCategory:
    @Debug(name='CreateCategory')
    def __call__(self, request):

        if request['method'] == 'POST':
            print(request)
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)
            site.categories.append(new_category)

            return '200 OK', render('index.html', object_list=site.categories)
        else:

            categories = site.categories
            return '200 OK', render('create_category.html', categories=categories)


@AppRoute(routes=routes, url='/category-list/')
class CategoryList:
    @Debug(name='CategoryList')
    def __call__(self, request):
        logger.log('список категорий')
        return '200 OK', render('category_list.html', object_list=site.categories)


@AppRoute(routes=routes, url='/copy-course/')
class CopyCourse:
    @Debug(name='CopyCourse')
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']
            old_course = site.get_course(name)
            if old_course:
                new_name = f'copy_{name}'
                new_course = old_course.clone()
                new_course.name = new_name
                site.courses.append(new_course)

            return '200 OK', render('course_list.html', object_list=site.courses)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


@AppRoute(routes=routes, url='/student-list/')
class StudentListView(ListView):
    template_name = 'student_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('student')
        return mapper.all()


@AppRoute(routes=routes, url='/create-student/')
class StudentCreateView(CreateView):
    template_name = 'create_student.html'

    def create_obj(self, data):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)
        new_obj.mark_new()
        UnitOfWork.get_current().commit()


@AppRoute(routes=routes, url='/add-student/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = site.get_student(student_name)
        course.add_student(student)


@AppRoute(routes=routes, url='/api/')
class CourseApi:
    @Debug(name='CourseApi')
    def __call__(self, request):
        for el in site.courses:
            print(f'course: {el.name}')
            for elem in el.students:
                print(f'user: {elem.name}')
        print(f'course category: {site.categories}')
        return '200 OK', BaseSerializer(site.courses).save()
