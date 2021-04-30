from datetime import date

from views import IndexView, AboutView, NotFound404View, StudyPrograms, CoursesList, CreateCourse, CreateCategory, \
    CategoryList, CopyCourse


def secret_front(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

# routes = {
#     '/': IndexView(),
#     '/about/': AboutView(),
#     '/study-programs/': StudyPrograms(),
#     '/courses-list/': CoursesList(),
#     '/create-course/': CreateCourse(),
#     '/create-category/': CreateCategory(),
#     '/category-list/': CategoryList(),
#     '/copy-course/': CopyCourse()
# }
