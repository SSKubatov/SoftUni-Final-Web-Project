import stripe
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from exam_web_project.courses.models import Course, Lesson
from exam_web_project.payments.models import Payment, UserCourseEnroll
from exam_web_project.core.utils.payments_utils import get_discounted_price
from exam_web_project.payments.services import StripeService, CourseEnrollmentService


UserModel = get_user_model()

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

stripe_service = StripeService()
course_enrollment_service = CourseEnrollmentService()


@login_required(login_url='sign in')
def checkout(request, slug):
    user = request.user
    course = get_object_or_404(Course, slug=slug)
    lessons = Lesson.objects.filter(course=course)
    error = None

    if request.method == "POST":
        succeed, message = course_enrollment_service.enroll_user_in_course(course, user)
        if succeed:
            session_url = stripe_service.create_checkout_session(course, user)
            return redirect(session_url, code=303)

        error = message

    context = {
        'course': course,
        'course_price': get_discounted_price(course.price, course.discount) / 100,
        'error': error,
        'lessons': lessons,
    }

    return render(request, 'payments/checkout.html', context)


def success(request):
    checkout_session_id = request.GET.get('session_id', None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    customer = stripe.Customer.retrieve(session.customer)

    context = {
        'customer': customer,
    }

    return render(request, 'payments/success.html', context)


def cancel(request):
    return render(request, 'payments/cancel.html')


@csrf_exempt
def webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        order_id = session['id']

        user_id = session['metadata']['user_id']
        user = UserModel.objects.get(id=user_id)

        course_id = session['metadata']['course_id']
        course = Course.objects.get(id=course_id)

        user_course = UserCourseEnroll.objects.create(
            user=user,
            course=course,
        )

        payment = Payment.objects.create(
            order_id=order_id,
            user=user,
            user_course=user_course,
            status=True,
        )

    return HttpResponse(status=200)
