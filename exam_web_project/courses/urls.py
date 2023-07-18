from django.urls import path, include

from exam_web_project.courses.views import course_page, CoursesShowcase, MyCourses, AdminCourseCreateView, \
    AdminCourseDeleteView, AdminLessonCreateView, AdminLessonDeleteView, AdminCourseLessonsView

urlpatterns = (
    path('my_courses/', MyCourses.as_view(), name='my courses'),
    path('courses-showcase/', CoursesShowcase.as_view(), name='courses showcase'),
    path('<str:slug>/', course_page, name='course page'),
    path('admin/courses/', include([
        path('create-course/', AdminCourseCreateView.as_view(), name='admin course create'),
        path('<slug:slug>/delete-course/', AdminCourseDeleteView.as_view(), name='admin course delete'),
        path('create-lesson/', AdminLessonCreateView.as_view(), name='admin lesson create'),
        path('delete-lesson/<int:pk>/', AdminLessonDeleteView.as_view(), name='admin lesson delete'),
        path('<slug:slug>/lessons/', AdminCourseLessonsView.as_view(), name='admin lessons display')
    ]))

)
