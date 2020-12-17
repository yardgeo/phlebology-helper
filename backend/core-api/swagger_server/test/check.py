import requests

session = requests.Session()
session.auth = ('orthancUser', 'orthancSecretPassword')

response = session.get('http://20.56.16.251:8042/patients/e95ff71a-c1d230d4-4373bc80-b595b6a2-5968f9d0')
print(response.json())