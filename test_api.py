import requests

url = "http://127.0.0.1:4444/account-applications"
data = {
    "title_of_account": "JOHN DOE",
    "name": "JOHN DOE",
    "cnic_no": "12345-1234567-1"
}

response = requests.post(url, json=data)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")