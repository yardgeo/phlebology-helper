# models
from swagger_server.models.patient import Patient  # noqa: E501
from swagger_server.models.study import Study  # noqa: E501


def patient_to_model(db_patient):
    return Patient(id=db_patient.id,
                   name=db_patient.name,
                   studies=[study_to_model(db_study) for db_study in db_patient.studies])


def study_to_model(db_study):
    return Study(id=db_study.id,
                 study_date=db_study.date)
