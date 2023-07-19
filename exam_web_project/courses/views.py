from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from django.views import generic as views

from exam_web_project.courses.forms import CourseForm, LessonForm, VideoForm
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


class CoursePageView(views.DetailView):
    model = Course
    template_name = "courses/course_page.html"
    context_object_name = "course"
    slug_url_kwarg = "slug"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        sorted_videos = self.object.video_set.all().order_by("serial_number")
        serial_number = request.GET.get('lecture', 1)
        video = self.get_video(serial_number)

        if not self.check_video_access(request, video):
            return self.handle_video_access_denied(request, video)

        resources = Resource.objects.filter(video=video)
        context = self.get_context_data(
            video=video,
            sorted_videos=sorted_videos,
            resources=resources
        )
        return self.render_to_response(context)

    def get_video(self, serial_number):
        course = self.object
        video = get_object_or_404(Video, serial_number=serial_number, course=course)
        return video

    def check_video_access(self, request, video):
        if not video.is_preview:
            user = request.user
            user_course_enroll = UserCourseEnroll.objects.filter(
                user=user,
                course=self.object
            ).exists()
            return request.user.is_authenticated and user_course_enroll
        return True

    def handle_video_access_denied(self, request, video):
        if not request.user.is_authenticated:
            return redirect('sign in')
        return redirect('checkout', slug=self.object.slug)


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


# <--------- LESSONS ------->
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


@method_decorator(login_required(login_url='sign in'), name='dispatch')
@method_decorator(user_passes_test(lambda user: user.is_staff), name='dispatch')
class AdminCourseLessonsView(views.TemplateView):
    template_name = 'courses/admin/course_lessons.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_slug = kwargs['slug']
        course = Course.objects.get(slug=course_slug)
        context['course'] = course
        context['lessons'] = course.lesson_set.all()
        return context


# <----------- VIDEOS --------------->
@method_decorator(login_required(login_url='sign in'), name='dispatch')
@method_decorator(user_passes_test(lambda user: user.is_staff), name='dispatch')
class AdminVideoCreateView(views.CreateView):
    model = Video
    form_class = VideoForm
    template_name = "courses/admin/video_create.html"

    def get_success_url(self):
        return reverse_lazy('courses showcase')


@method_decorator(login_required(login_url='sign in'), name='dispatch')
@method_decorator(user_passes_test(lambda user: user.is_staff), name='dispatch')
class AdminVideoDeleteView(views.DeleteView):
    model = Video
    template_name = "courses/admin/video_delete.html"
    success_url = reverse_lazy('courses showcase')


@method_decorator(login_required(login_url='sign in'), name='dispatch')
@method_decorator(user_passes_test(lambda user: user.is_staff), name='dispatch')
class AdminCourseVideoView(views.TemplateView):
    template_name = 'courses/admin/course_videos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_slug = kwargs['slug']
        course = Course.objects.get(slug=course_slug)
        context['videos'] = course.video_set.all()
        context['course'] = course
        return context
