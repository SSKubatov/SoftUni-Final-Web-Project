import stripe
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from exam_web_project.courses.models import Course, Lesson
from exam_web_project.payments.models import Payment
from core.utils.payments_utils import get_discounted_price
from exam_web_project.payments.services import StripeService, CourseEnrollmentService

UserModel = get_user_model()

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


@login_required
def checkout(request, slug):
    ALREADY_SUBSCRIBED_MESSAGE = "You are already purchased this course."

    user = request.user
    course = get_object_or_404(Course, slug=slug)
    lessons = Lesson.objects.filter(course=course)

    if request.method == "POST":
        stripe_services = StripeService()
        course_enrollment_service = CourseEnrollmentService(user, course)

        session_url = stripe_services.create_checkout_session(course, user)
        order_id = stripe_services.get_checkout_session_id
        user_already_enroll = course_enrollment_service.check_if_user_enroll_in_course()

        if user_already_enroll:
            messages.error(request, ALREADY_SUBSCRIBED_MESSAGE)
            return redirect('courses showcase')

        Payment.objects.create(order_id=order_id, user=user)

        return redirect(session_url, code=303)

    context = {
        'course': course,
        'course_price': get_discounted_price(course.price, course.discount) / 100,
        'lessons': lessons,
    }

    return render(request, 'payments/checkout.html', context)


def success(request):
    checkout_session_id = request.GET.get('session_id', None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    customer = stripe.Customer.retrieve(session.customer)

    user_id = session['metadata']['user_id']
    user = get_object_or_404(UserModel, id=user_id)

    course_id = session['metadata']['course_id']
    course = get_object_or_404(Course, id=course_id)

    course_enrollment_service = CourseEnrollmentService(user, course)
    user_course = course_enrollment_service.enroll_user_to_course()

    payment = Payment.objects.get(order_id=checkout_session_id)
    payment.enroll_user_to_course(user_course)
    payment.mark_as_paid()

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
        user = get_object_or_404(UserModel, id=user_id)

        course_id = session['metadata']['course_id']
        course = get_object_or_404(Course, id=course_id)

        course_enrollment_service = CourseEnrollmentService(user, course)
        user_course = course_enrollment_service.enroll_user_to_course()

        payment = Payment.objects.get(order_id=order_id)
        payment.user_course = user_course
        payment.save()

    return HttpResponse(status=200)
