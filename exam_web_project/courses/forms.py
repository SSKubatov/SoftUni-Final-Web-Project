from crispy_forms import helper as crispy_helper
from crispy_forms import layout as crispy_layout
from django import forms

from exam_web_project.courses.models import Course, Lesson


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = crispy_helper.FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(crispy_layout.Submit('submit', 'Save'))


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = crispy_helper.FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(crispy_layout.Submit('submit', 'Save'))
