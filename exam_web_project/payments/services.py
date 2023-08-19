import os
import stripe
from django.urls import reverse

from core.utils.payments_utils import get_discounted_price_rounded_to_thousands
from exam_web_project.payments.models import UserCourseEnroll


class StripeService:

    def __init__(self):
        self._session_id = None

    def create_checkout_session(self, course, user):
        success_url = os.environ.get('MY_DOMAIN') + reverse('success') + '?session_id={CHECKOUT_SESSION_ID}'
        cancel_url = os.environ.get('MY_DOMAIN') + reverse('cancel')
        course_price = get_discounted_price_rounded_to_thousands(course.price, course.discount)

        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'bgn',
                    'product_data': {
                        'name': course.name,
                    },
                    'unit_amount': course_price,
                },
                'quantity': 1,
            }],
            mode='payment',
            customer_creation='always',
            metadata={
                'course_id': course.id,
                'user_id': user.id,
            },
            success_url=success_url,
            cancel_url=cancel_url,
            automatic_tax={
                'enabled': True
            },
        )

        self._session_id = session.id
        return session.url

    @property
    def session_id(self):
        return self._session_id

    @session_id.setter
    def session_id(self, value):
        self._session_id = value


class CourseEnrollmentService:

    def __init__(self, user, course):
        self.user = user
        self.course = course

    def check_if_user_enroll_in_course(self):
        return UserCourseEnroll.objects.filter(user=self.user, course=self.course).exists()

    def enroll_user_to_course(self):
        user_already_enrolled = self.check_if_user_enroll_in_course()

        if not user_already_enrolled:
            return UserCourseEnroll.objects.create(user=self.user, course=self.course)
