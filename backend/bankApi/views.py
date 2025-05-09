import stripe
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Transaction  # Assuming Transaction is the model for rental requests
import hmac
import hashlib
import base64
import random
import string

class StripePaymentIntentView(APIView):
    """
    Handles creating and retrieving Stripe payment intents.
    """

    @swagger_auto_schema(
        operation_description="Create a new Stripe payment intent",
        tags=["Stripe Payment Intent"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'amount': openapi.Schema(type=openapi.TYPE_INTEGER, description='Amount in cents'),
            },
            required=['amount']
        ),
        responses={
            200: openapi.Response(
                description="Payment intent created successfully",
                examples={
                    "application/json": {
                        "clientSecret": "pi_1J2m3L2eZvKYlo2C0X1Y2Z3A_secret_4J2m3L2eZvKYlo2C0X1Y2Z3A",
                        "paymentIntentId": "pi_1J2m3L2eZvKYlo2C0X1Y2Z3A",
                        "amount": 1000,
                        "currency": "usd",
                        "status": "requires_payment_method",
                        "created": 1625256000,
                        "payment_method_types": ["card"]
                    }
                }
            ),
            400: "Bad Request"
        }
    )
    def post(self, request):
        """
        Create a new Stripe payment intent.   
        """
        stripe.api_key = settings.STRIPE_SECRET_KEY
        amount = request.data.get("amount", 0)

        try:
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency="usd",
                payment_method_types=["card"],
            )
            request.session['payment_intent_id'] = intent["id"]
            return JsonResponse({
                "clientSecret": intent["client_secret"],
                "paymentIntentId": intent["id"],
                "amount": intent["amount"],
                "currency": intent["currency"],
                "status": intent["status"],
                "created": intent["created"],
                "payment_method_types": intent["payment_method_types"],
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    @swagger_auto_schema(
        operation_description="Retrieve an existing Stripe payment intent",
        tags=["Stripe Payment Intent"],
        responses={
            200: openapi.Response(
                description="Payment intent retrieved successfully",
                examples={
                    "application/json": {
                        "id": "pi_1J2m3L2eZvKYlo2C0X1Y2Z3A",
                        "amount": 1000,
                        "currency": "usd",
                        "status": "requires_payment_method",
                        "created": 1625256000,
                        "payment_method_types": ["card"]
                    }
                }
            ),
            400: "Bad Request"
        }
    )
    def get(self, request):
        """
        Retrieve an existing Stripe payment intent.
        """
        stripe.api_key = settings.STRIPE_SECRET_KEY
        payment_intent_id = request.session.get('payment_intent_id')

        if not payment_intent_id:
            return JsonResponse({"error": "No Payment Intent ID found in session."}, status=400)

        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            return JsonResponse({
                "id": intent["id"],
                "amount": intent["amount"],
                "currency": intent["currency"],
                "status": intent["status"],
                "created": intent["created"],
                "payment_method_types": intent["payment_method_types"],
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@login_required
def confirm_requests(request):
    """
    Fetch approved requests for the tenant and generate eSewa payment fields.
    """
    user = request.user

    # Fetch approved requests for the tenant
    approved_requests = Transaction.objects.filter(
        tenant_id=user.id,
        status='approved'
    ).order_by('-date_created')

    for transaction in approved_requests:
        # Generate eSewa payment fields
        payment_fields = generate_esewa_payment_fields(transaction)
        transaction.uuid = payment_fields['uuid']
        transaction.signed_field_names = payment_fields['signed_field_names']
        transaction.signature = payment_fields['signature']

    return render(request, 'bankApi/confirm_request_payment.html', {'approved_requests': approved_requests})


def generate_esewa_payment_fields(transaction):
    """
    Generate eSewa payment fields for a transaction.
    """
    secret_key = "8gBm/:&EnhH.1/q"
    uuid_value = generate_short_uuid(12)  # Generate UUID
    total_amount = transaction.total_price
    product_code = "EPAYTEST"

    signed_fields = "total_amount,transaction_uuid,product_code"
    data = f"total_amount={total_amount},transaction_uuid={uuid_value},product_code={product_code}"

    signature = base64.b64encode(
        hmac.new(secret_key.encode(), data.encode(), hashlib.sha256).digest()
    ).decode()

    return {
        'uuid': uuid_value,
        'signed_field_names': signed_fields,
        'signature': signature
    }


def generate_short_uuid(length=12):
    """
    Generate a short UUID of the specified length.
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


@login_required
def payment_success(request, request_id=None):
    """
    Handle successful payments and log them in the database.
    """
    user = request.user
    amount = request.GET.get('amount', 0)  # Assuming amount is passed as a query parameter
    transaction_id = request.GET.get('transaction_id', '')  # Assuming transaction_id is passed as a query parameter

    # Log the successful payment
    transaction, created = Transaction.objects.get_or_create(
        transaction_id=transaction_id,
        defaults={
            'user': user,
            'amount': amount,
            'status': 'success',
        }
    )

    if not created:
        transaction.status = 'success'
        transaction.save()

    return JsonResponse({"message": f"Payment successful for request ID: {request_id}", "transaction_id": transaction_id})


@login_required
def payment_fail(request):
    """
    Handle failed payments and log them in the database.
    """
    user = request.user
    amount = request.GET.get('amount', 0)  # Assuming amount is passed as a query parameter
    transaction_id = request.GET.get('transaction_id', '')  # Assuming transaction_id is passed as a query parameter

    # Log the failed payment
    transaction, created = Transaction.objects.get_or_create(
        transaction_id=transaction_id,
        defaults={
            'user': user,
            'amount': amount,
            'status': 'failed',
        }
    )

    if not created:
        transaction.status = 'failed'
        transaction.save()

    return JsonResponse({"message": "Payment failed. Please try again.", "transaction_id": transaction_id})


@csrf_exempt
@method_decorator(csrf_exempt, name='dispatch')
def esewa_webhook(request):
    """
    Handle eSewa payment notifications.
    """
    if request.method == 'POST':
        transaction_id = request.POST.get('transaction_id')
        status = request.POST.get('status')
        amount = request.POST.get('amount')

        try:
            transaction = Transaction.objects.get(transaction_id=transaction_id)
            transaction.status = status
            transaction.amount = amount
            transaction.save()
            return JsonResponse({"message": "Transaction updated successfully."})
        except Transaction.DoesNotExist:
            return JsonResponse({"error": "Transaction not found."}, status=404)

    return JsonResponse({"error": "Invalid request method."}, status=400)


@login_required  # Ensure the user is authenticated
@csrf_exempt  # Disable CSRF protection for this view
def initiate_esewa_payment(request):
    """
    Initiate an eSewa payment and save the transaction.
    """
    if not request.user.is_authenticated:
        return JsonResponse({"error": "User must be authenticated to initiate a payment."}, status=401)

    user = request.user
    amount = request.POST.get('amount')
    if not amount:
        return JsonResponse({"error": "Amount is required."}, status=400)

    transaction_id = generate_short_uuid(12)

    # Save the transaction
    transaction = Transaction.objects.create(
        user=user,
        transaction_id=transaction_id,
        amount=amount,
        status='initiated'
    )

    # Redirect to eSewa payment gateway
    esewa_url = f"https://esewa.com.np/epay/main?amt={amount}&pid={transaction_id}&scd=EPAYTEST&su=http://yourdomain.com/success&fu=http://yourdomain.com/fail"
    return JsonResponse({"esewa_url": esewa_url})