import requests

url = "http://127.0.0.1:8000/crud/transactions/all/"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ2MzQwODk5LCJpYXQiOjE3NDYzMzk5OTksImp0aSI6ImNiMmE3ODgxZDY4ODQ3Yjg5ZDMwYWMzOTUxOWRiNWEzIiwidXNlcl9pZCI6NX0.dvaHMTr-hUXSWNAP8kJS8uAaN356oZeyAgDlzavWRMs"
}

response = requests.get(url, headers=headers)
print(response.json())