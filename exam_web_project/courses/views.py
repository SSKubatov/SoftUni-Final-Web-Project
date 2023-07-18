from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from django.views import generic as views

from exam_web_project.courses.forms import CourseForm, LessonForm
from exam_web_project.courses.models import Course, Video, Resource, Lesson
from exam_web_project.payments.models import UserCourseEnroll


class CoursesShowcase(views.ListView):
    template_name = 'courses/courses_showcase.html'
    queryset = Course.objects.all().order_by('created_at')
    context_object_name = 'courses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            enrolled_courses = UserCourseEnroll.objects.filter(user=self.request.user).values_list('course', flat=True)
            context['enrolled_courses'] = enrolled_courses

        return context


@method_decorator(login_required(login_url='sign in'), name='dispatch')
class MyCourses(views.ListView):
    template_name = 'courses/my_courses.html'
    context_object_name = 'user_courses'

    def get_queryset(self):
        return UserCourseEnroll.objects.filter(user=self.request.user)


def course_page(request, slug):
    course = get_object_or_404(Course, slug=slug)

    serial_number = request.GET.get('lecture')

    if serial_number is None:
        serial_number = 1

    video = get_object_or_404(Video, serial_number=serial_number, course=course)
    sorted_videos = course.video_set.all().order_by("serial_number")

    if not video.is_preview:
        if not request.user.is_authenticated:
            return redirect('sign in')

        user = request.user
        user_course_enroll = UserCourseEnroll.objects.filter(
            user=user,
            course=course
        ).exists()

        if not user_course_enroll:
            return redirect('checkout', slug=slug)

    resources = Resource.objects.filter(
        video=video,
    )

    context = {
        'course': course,
        'video': video,
        'sorted_videos': sorted_videos,
        'resources': resources,
    }

    return render(request, "courses/course_page.html", context)


# ADMIN Views

@method_decorator(login_required(login_url='sign in'), name='dispatch')
@method_decorator(user_passes_test(lambda user: user.is_staff), name='dispatch')
class AdminCourseCreateView(views.CreateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/admin/course_create.html"

    def get_success_url(self):
        return reverse_lazy('courses showcase')


@method_decorator(login_required(login_url='sign in'), name='dispatch')
@method_decorator(user_passes_test(lambda user: user.is_staff), name='dispatch')
class AdminCourseDeleteView(views.DeleteView):
    model = Course
    template_name = "courses/admin/course_delete.html"
    success_url = reverse_lazy('courses showcase')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(success_url)


@method_decorator(login_required(login_url='sign in'), name='dispatch')
@method_decorator(user_passes_test(lambda user: user.is_staff), name='dispatch')
class AdminLessonCreateView(views.CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = "courses/admin/lesson_create.html"

    def get_success_url(self):
        return reverse_lazy('courses showcase')


@method_decorator(login_required(login_url='sign in'), name='dispatch')
@method_decorator(user_passes_test(lambda user: user.is_staff), name='dispatch')
class AdminLessonDeleteView(views.DeleteView):
    model = Lesson
    success_url = reverse_lazy('courses showcase')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return redirect(success_url)


class AdminCourseLessonsView(views.TemplateView):
    template_name = 'courses/admin/course_lessons.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_slug = kwargs['slug']
        course = Course.objects.get(slug=course_slug)
        lessons = Lesson.objects.filter(course=course)
        context['course'] = course
        context['lessons'] = lessons
        return context
