from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from .views import StripePaymentIntentView, confirm_requests, payment_success, payment_fail, initiate_esewa_payment, esewa_webhook

# Swagger schema view configuration
schema_view = get_schema_view(
    openapi.Info(
        title="Bank API",
        default_version='v1',
        description="API documentation for the Bank API app",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@bankapi.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    # Swagger and ReDoc URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # Bank API endpoints
    path('payment-intent/', StripePaymentIntentView.as_view(), name='stripe-payment-intent'),
    path('confirm-requests/', confirm_requests, name='confirm-requests'),
    path('payment-success/', payment_success, name='payment-success-no-id'),
    path('payment-success/<int:request_id>/', payment_success, name='payment-success'),
    path('payment-fail/', payment_fail, name='payment-fail'),

    # eSewa payment initiation and webhook
    path('initiate-esewa-payment/', initiate_esewa_payment, name='initiate-esewa-payment'),
    path('esewa-webhook/', esewa_webhook, name='esewa-webhook'),
]