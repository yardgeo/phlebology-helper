import requests
from io import BytesIO
# config & utils
from config import Config
# logger
from swagger_server import logger
import base64

# config parameters
ORTHANC_USER = Config.ORTHANC_USER
ORTHANC_PASSWORD = Config.ORTHANC_PASSWORD
ORTHANC_URL = Config.ORTHANC_URL


class OrthancClient:
    def __init__(self,
                 user=ORTHANC_USER,
                 password=ORTHANC_PASSWORD,
                 base_url=ORTHANC_URL):

        self.session = requests.Session()
        self.session.auth = (user, password)
        self.base_url = base_url

    def get_patients(self):
        response = self.session.get(self.base_url + 'patients/')
        return response.json()

    def get_patient_by_id(self, patient_id):
        response = self.session.get(self.base_url + 'patients/' + patient_id)
        return response.json()

    def get_study_by_id(self, study_id):
        response = self.session.get(self.base_url + 'studies/' + study_id)
        return response.json()

    def get_series_by_id(self, series_id):
        response = self.session.get(self.base_url + 'series/' + series_id)
        return response.json()

    def download_dicom_by_id(self, instance_id):
        response = self.session.get(self.base_url + 'instances/' + instance_id + "/file")
        return BytesIO(response.content)

    def download_preview_by_id(self, instance_id):
        response = self.session.get(self.base_url + 'instances/' + instance_id + "/preview",
                                    headers={'Accept': 'image/jpeg'})
        decoded_blob = base64.b64encode(response.content).decode()
        return "data:image/jpeg;base64," + decoded_blob


orthancClient = OrthancClient()
