from django.urls import path, include

from exam_web_project.courses.views import course_page, CoursesShowcase, MyCourses, AdminCourseCreateView, \
    AdminCourseDeleteView

urlpatterns = (
    path('my_courses/', MyCourses.as_view(), name='my courses'),
    path('courses-showcase/', CoursesShowcase.as_view(), name='courses showcase'),
    path('<str:slug>/', course_page, name='course page'),
    path('admin/courses/', include([
        path('create/', AdminCourseCreateView.as_view(), name='admin course create'),
        path('<slug:slug>/delete/', AdminCourseDeleteView.as_view(), name='admin course delete'),
    ]))

)
