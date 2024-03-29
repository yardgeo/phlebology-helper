import connexion
import six

from swagger_server import util

# services
import swagger_server.services.patient_service as patient_service
import swagger_server.services.converter_service as converter_service

from flask import send_file


def get_patient(id):  # noqa: E501
    """Get patient by id

     # noqa: E501

    :param id: Patient id
    :type id: str

    :rtype: None
    """
    db_patient = patient_service.get_patient_by_id(id)
    return converter_service.patient_to_model(db_patient)


def get_patients_ids():  # noqa: E501
    """Get patients ids

     # noqa: E501


    :rtype: None
    """

    patients = patient_service.get_patients()

    return [converter_service.patient_to_model(db_patient) for db_patient in patients]


def get_studies(patientId):  # noqa: E501
    """Get patients ids

     # noqa: E501


    :rtype: None
    """

    studies = patient_service.get_studies(patientId)
    return [converter_service.study_to_model(db_study) for db_study in studies]
