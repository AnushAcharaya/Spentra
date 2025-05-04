import requests

url = "http://127.0.0.1:8000/crud/transactions/all/"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ2MzQ0MDY4LCJpYXQiOjE3NDYzNDMxNjgsImp0aSI6IjY0NTM0NzcxOWM0ODQxZWJhNjI0MmY1ZTcwMjFiYzdkIiwidXNlcl9pZCI6NX0.1ep4tWN5zOmB10oEQI5aCoFikyIuNCwMra-YeroNLXk"
}

response = requests.get(url, headers=headers)
print(response.json())