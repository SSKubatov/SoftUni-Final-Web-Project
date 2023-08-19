from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from django.views import generic as views

from exam_web_project.courses.forms import CourseForm, LessonForm, VideoForm
from exam_web_project.courses.models import Course, Video, Resource, Lesson
from exam_web_project.payments.models import UserCourseEnroll, Payment


class CoursesShowcaseView(views.ListView):
    template_name = 'courses/courses_showcase.html'
    queryset = Course.objects.all().order_by('created_at')
    context_object_name = 'courses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_staff and self.request.user.is_active:
            context['is_staff'] = True
        elif self.request.user.is_authenticated:
            enrolled_courses = UserCourseEnroll.objects.filter(user=self.request.user).values_list('course', flat=True)
            context['enrolled_courses'] = enrolled_courses

        return context


class MyCoursesView(LoginRequiredMixin, views.ListView):
    template_name = 'courses/my_courses.html'
    context_object_name = 'user_courses'

    def get_queryset(self):
        user = self.request.user
        return UserCourseEnroll.objects.filter(user=user)


class CoursePageView(views.DetailView):
    model = Course
    template_name = "courses/course_page.html"
    context_object_name = "course"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        course = self.object
        sorted_videos = self.object.video_set.all().order_by("serial_number")
        serial_number = request.GET.get('lecture', 1)
        video = get_object_or_404(Video, serial_number=serial_number, course=course)
        resources = Resource.objects.filter(video=video)

        try:
            user_course = get_object_or_404(UserCourseEnroll, user=self.request.user, course=course)
            payment = Payment.objects.get(user=self.request.user, user_course=user_course)
            if payment.status:
                video.is_preview = True

            return self.custom_context_render(video, sorted_videos, resources)
        except:
            if self.request.user.is_staff and self.request.user.is_active:
                pass
            elif not video.is_preview:
                return self.handle_video_access_denied(request)
            return self.custom_context_render(video, sorted_videos, resources)

    def handle_video_access_denied(self, request):
        user = request.user.is_authenticated
        if not user:
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('sign in')
        return redirect('checkout', slug=self.object.slug)

    def custom_context_render(self, video, sorted_videos, resources):
        context = self.get_context_data(
            video=video,
            sorted_videos=sorted_videos,
            resources=resources
        )
        return self.render_to_response(context)


# ADMIN Views

class AdminCourseCreateView(LoginRequiredMixin, UserPassesTestMixin, views.CreateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/admin/course_create.html"

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_success_url(self):
        return reverse_lazy('courses showcase')


class AdminCourseDeleteView(LoginRequiredMixin, UserPassesTestMixin, views.DeleteView):
    model = Course
    template_name = "courses/admin/course_delete.html"
    success_url = reverse_lazy('courses showcase')

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(success_url)


# <--------- LESSONS ------->

class AdminLessonCreateView(LoginRequiredMixin, UserPassesTestMixin, views.CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = "courses/admin/lesson_create.html"

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_success_url(self):
        return reverse_lazy('courses showcase')


class AdminLessonDeleteView(LoginRequiredMixin, UserPassesTestMixin, views.DeleteView):
    model = Lesson
    success_url = reverse_lazy('courses showcase')

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return redirect(success_url)


class AdminCourseLessonsView(LoginRequiredMixin, UserPassesTestMixin, views.TemplateView):
    template_name = 'courses/admin/course_lessons.html'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_slug = kwargs['slug']
        course = Course.objects.get(slug=course_slug)
        context['course'] = course
        context['lessons'] = course.lesson_set.all()
        return context


# <----------- VIDEOS --------------->

class AdminVideoCreateView(LoginRequiredMixin, UserPassesTestMixin, views.CreateView):
    model = Video
    form_class = VideoForm
    template_name = "courses/admin/video_create.html"

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_success_url(self):
        return reverse_lazy('courses showcase')


class AdminVideoDeleteView(LoginRequiredMixin, UserPassesTestMixin, views.DeleteView):
    model = Video
    template_name = "courses/admin/video_delete.html"
    success_url = reverse_lazy('courses showcase')

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


class AdminCourseVideoView(LoginRequiredMixin, UserPassesTestMixin, views.TemplateView):
    template_name = 'courses/admin/course_videos.html'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_slug = kwargs['slug']
        course = Course.objects.get(slug=course_slug)
        context['videos'] = course.video_set.all()
        context['course'] = course
        return context
