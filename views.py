from datetime import date

from mosquito_framework.templator import render
from patterns.creational_patterns import Engine, Logger

site = Engine()
logger = Logger('main')


class IndexView:
    def __call__(self, request):
        return '200 OK', render('index.html', object_list=site.categories)


class AboutView:
    def __call__(self, request):
        return '200 OK', render('contact.html')


class NotFound404View:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class StudyPrograms:
    def __call__(self, request):
        return '200 OK', render('study-programs.html', data=date.today())


class CoursesList:
    def __call__(self, request):
        logger.log('список курсов')
        try:
            category = site.find_category_by_id(int(request['request_params']['id']))
            return '200 OK', render('course_list.html', object_list=category.courses, name=category.name,
                                    id=category.id)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


class CreateCourse:
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course('offline', name, category)
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


class CreateCategory:
    def __call__(self, request):
        print(f'{request}request')

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


class CategoryList:
    def __call__(self, request):
        logger.log('список категорий')
        return '200 OK', render('category_list.html', object_list=site.categories)


class CopyCourse:
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
