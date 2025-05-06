import requests
from django.http import JsonResponse
from django.conf import settings

class KhaltiVerifyView:
    def post(self, request):
        # Get the token and amount from the frontend
        token = request.POST.get('token')
        amount = request.POST.get('amount')

        # Khalti verification URL
        khalti_verify_url = "https://khalti.com/api/v2/payment/verify/"

        # Headers and payload for the verification request
        headers = {
            "Authorization": f"Key {settings.KHALTI_SECRET_KEY}"
        }
        payload = {
            "token": token,
            "amount": amount
        }

        # Send the verification request to Khalti
        response = requests.post(khalti_verify_url, headers=headers, data=payload)

        # Check the response from Khalti
        if response.status_code == 200:
            return JsonResponse({"status": "success", "message": "Payment verified successfully.", "data": response.json()})
        else:
            return JsonResponse({"status": "failure", "message": "Payment verification failed.", "data": response.json()}, status=400)