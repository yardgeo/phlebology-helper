import requests
import datetime
from io import BytesIO

# db
from swagger_server.app import db
from swagger_server.db_models import Patient, Study

# config & utils
from config import Config

# config parameters
ORTHANC_USER = Config.ORTHANC_USER
ORTHANC_PASSWORD = Config.ORTHANC_PASSWORD
ORTHANC_URL = Config.ORTHANC_URL


def get_patients():
    session = requests.Session()
    session.auth = (ORTHANC_USER, ORTHANC_PASSWORD)

    response = session.get(ORTHANC_URL + 'patients/')
    patient_ids = response.json()

    db_patient_ids = [patient.id for patient in db.session().query(Patient).all()]

    for patient_id in set(patient_ids).difference(set(db_patient_ids)):
        response = session.get(ORTHANC_URL + 'patients/' + patient_id)
        orthanc_patient = response.json()
        db.session().add(Patient(id=patient_id,
                                 name=orthanc_patient.get("MainDicomTags").get("PatientName")))

    db.session().commit()

    return db.session().query(Patient).all()


def get_patient_by_id(id):
    get_studies(id)
    return db.session().query(Patient).filter(Patient.id == id).first()


def get_studies(patient_id):
    session = requests.Session()
    session.auth = (ORTHANC_USER, ORTHANC_PASSWORD)

    response = session.get(ORTHANC_URL + 'patients/' + patient_id)
    study_ids = response.json().get("Studies")

    patient = db.session().query(Patient).filter(Patient.id == patient_id).first()

    studies = db.session().query(Study).filter(Study.patient_id == patient_id).all()

    db_study_ids = [study.id for study in studies]

    for study_id in set(study_ids).difference(set(db_study_ids)):
        response = session.get(ORTHANC_URL + 'studies/' + study_id)
        orthanc_study = response.json()
        date = orthanc_study.get("MainDicomTags").get("StudyDate")
        date = datetime.datetime.strptime(date, "%Y%m%d").date().isoformat()
        db.session().add(Study(id=study_id,
                               date=date,
                               patient=patient))

    db.session().commit()

    return db.session().query(Study).filter(Study.patient_id == patient_id).all()


def get_study_by_id(id):
    return db.session().query(Study).filter(Study.id == id).first()


def get_media(study_id):
    session = requests.Session()
    session.auth = (ORTHANC_USER, ORTHANC_PASSWORD)

    response = session.get(ORTHANC_URL + 'studies/' + study_id + "/media")
    return BytesIO(response.content)
