import datetime
import json

# db
from swagger_server.app import db
from swagger_server.db_models import Patient, Study, Instance, Series

# services
from swagger_server.services.orthanc_service import orthancClient

# logger
from swagger_server import logger


def get_patients():
    patient_ids = orthancClient.get_patients()

    db_patient_ids = [patient.id for patient in db.session().query(Patient).all()]

    for patient_id in set(patient_ids).difference(set(db_patient_ids)):
        orthanc_patient = orthancClient.get_patient_by_id(patient_id=patient_id)
        db.session().add(Patient(id=patient_id,
                                 name=orthanc_patient.get("MainDicomTags").get("PatientName")))

    db.session().commit()

    return db.session().query(Patient).all()


def get_patient_by_id(id):
    get_studies(id)
    return db.session().query(Patient).filter(Patient.id == id).first()


def get_studies(patient_id):
    study_ids = orthancClient.get_patient_by_id(patient_id=patient_id).get("Studies")

    db_patient = Patient.query.filter(Patient.id == patient_id).first()

    db_studies = []
    if db_patient:
        db_studies = db_patient.studies

    db_study_ids = [study.id for study in db_studies]

    for study_id in set(study_ids).difference(set(db_study_ids)):
        orthanc_study = orthancClient.get_study_by_id(study_id=study_id)
        date = orthanc_study.get("MainDicomTags").get("StudyDate")

        date = datetime.datetime.strptime(date, "%Y%m%d").date().isoformat()
        db_study = Study(id=study_id,
                         date=date,
                         description=orthanc_study.get("MainDicomTags").get("StudyDescription"),
                         patient=db_patient)
        db.session().add(db_study)

    db.session().commit()

    return db.session().query(Study).filter(Study.patient_id == patient_id).all()


def get_series(study_id):
    series_ids = orthancClient.get_study_by_id(study_id=study_id).get("Series")

    db_study = Study.query.filter(Study.id == study_id).first()
    db_series = []

    if db_study:
        db_series = db_study.series

    db_series_ids = [s.id for s in db_series]
    for series_id in set(series_ids).difference(set(db_series_ids)):
        series = orthancClient.get_series_by_id(series_id)
        db.session().add(Series(id=series_id,
                                study_id=study_id,
                                orientation=series.get("MainDicomTags").get("ImageOrientationPatient")))

        instances = series.get("Instances")
        for i, instance in enumerate(instances):
            db.session().add(Instance(id=instance,
                                      order=i,
                                      preview=orthancClient.download_preview_by_id(instance),
                                      series_id=series_id))

    db.session().commit()
    return Series.query.filter(Series.study_id == study_id).all()


def get_series_by_id(id):
    return Series.query.filter(Series.id == id).first()


def get_study_by_id(id):
    get_series(study_id=id)
    return Study.query.filter(Study.id == id).first()


def get_dicom_media(id):
    return orthancClient.download_dicom_by_id(instance_id=id)


def preview(id):
    return orthancClient.download_preview_by_id(instance_id=id)


def upload_original_state(series_id, state):
    db_series = Series.query.filter(Series.id == series_id).first()

    if db_series is None:
        return False

    db_series.original_state = json.dumps(state)
    db.session().commit()


def get_original_state(series_id):
    db_series = Series.query.filter(Series.id == series_id).first()

    if not db_series.original_state:
        return None

    return json.loads(db_series.original_state)
