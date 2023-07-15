import stripe
from django.urls import reverse

from exam_web_project import settings
from exam_web_project.core.utils.payments_utils import get_discounted_price
from exam_web_project.payments.models import UserCourseEnroll


class StripeService:
    MY_DOMAIN = 'http://127.0.0.1:8000'

    def __init__(self):
        self.stripe_api_key = stripe.api_key

    def create_checkout_session(self, course, user):
        course_price = get_discounted_price(course.price, course.discount)
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
            success_url=self.MY_DOMAIN + reverse('success') + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=self.MY_DOMAIN + reverse('cancel'),
            automatic_tax={
                'enabled': True
            },
        )

        return session.url


class CourseEnrollmentService:
    ENROLL_SUCCESS_MESSAGE = 'Enrollment successful'
    ENROLL_FAIL_MESSAGE = 'You are already enrolled in this course'

    def enroll_user_in_course(self, course, user):
        user_course_enroll = UserCourseEnroll.objects.filter(user=user, course=course).exists()

        if user_course_enroll:
            return False, self.ENROLL_SUCCESS_MESSAGE
        else:
            UserCourseEnroll.objects.create(user=user, course=course)
            return True, self.ENROLL_FAIL_MESSAGE
