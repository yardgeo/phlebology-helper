import requests
from io import BytesIO

# TODO REWORK
def get_patients():
    session = requests.Session()
    session.auth = ('orthancUser', 'orthancSecretPassword')

    response = session.get('http://20.56.16.251:8042/patients')
    return response.json()


def get_patient_by_id(id):
    session = requests.Session()
    session.auth = ('orthancUser', 'orthancSecretPassword')

    response = session.get('http://20.56.16.251:8042/patients/' + id)
    return response.json()


def preview():
    session = requests.Session()
    session.auth = ('orthancUser', 'orthancSecretPassword')

    response = session.get('http://20.56.16.251:8042/instances/5fdd7a0a-2830d53a-1d754883-97a27596-c834e770/preview')
    return BytesIO(response.content)