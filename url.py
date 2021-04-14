from views import IndexView, AboutView, NotFoundPage404View, Other

routes = {
    '/': IndexView(),
    '/about/': AboutView(),
    '/other/': Other(),
}
