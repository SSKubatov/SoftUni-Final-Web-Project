from django.urls import path, include
from exam_web_project.courses.views import CoursePageView, CoursesShowcaseView, MyCoursesView, AdminCourseCreateView, \
    AdminCourseDeleteView, AdminLessonCreateView, AdminLessonDeleteView, AdminCourseLessonsView, AdminVideoCreateView, \
    AdminCourseVideoView, AdminVideoDeleteView

urlpatterns = (
    path('my_courses/', MyCoursesView.as_view(), name='my courses'),
    path('courses-showcase/', CoursesShowcaseView.as_view(), name='courses showcase'),
    path('<slug:slug>/', CoursePageView.as_view(), name='course page'),
    path('admin/courses/', include([
        path('create-course/', AdminCourseCreateView.as_view(), name='admin course create'),
        path('<slug:slug>/delete-course/', AdminCourseDeleteView.as_view(), name='admin course delete'),
        path('lessons/', include([
            path('create-lesson/', AdminLessonCreateView.as_view(), name='admin lesson create'),
            path('delete-lesson/<int:pk>/', AdminLessonDeleteView.as_view(), name='admin lesson delete'),
            path('<slug:slug>/lessons-display/', AdminCourseLessonsView.as_view(), name='admin lessons display')
        ])),
        path('videos/', include([
            path('create-video/', AdminVideoCreateView.as_view(), name='admin video create'),
            path('delete-lesson/<int:pk>/', AdminVideoDeleteView.as_view(), name='admin video delete'),
            path('<slug:slug>/videos-display/', AdminCourseVideoView.as_view(), name='admin video display')
        ]))

    ]))

)
