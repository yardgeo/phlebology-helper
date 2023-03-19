# models
from swagger_server.models.patient import Patient  # noqa: E501
from swagger_server.models.study import Study  # noqa: E501
from swagger_server.models.series import Series  # noqa: E501
from swagger_server.models.instance import Instance


def patient_to_model(db_patient):
    return Patient(id=db_patient.id,
                   name=db_patient.name,
                   studies=[study_to_model(db_study) for db_study in db_patient.studies])


def study_to_model(db_study):
    return Study(id=db_study.id,
                 study_date=db_study.date,
                 series=[series_to_model(db_series) for db_series in db_study.series],
                 description=db_study.description)


def series_to_model(db_series):
    return Series(id=db_series.id,
                  orientation=db_series.orientation,
                  has_state=db_series.original_state is not None,
                  instances=[instance_to_model(db_instance) for db_instance in db_series.instances])


def instance_to_model(db_instance):
    return Instance(id=db_instance.id,
                    preview=db_instance.preview)
