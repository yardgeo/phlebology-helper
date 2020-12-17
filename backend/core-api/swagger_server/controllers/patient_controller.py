import connexion
import six

from swagger_server import util

# services
import swagger_server.services.patient_service as patient_service

from flask import send_file


def get_patient(id):  # noqa: E501
    """Get patient by id

     # noqa: E501

    :param id: Patient id
    :type id: str

    :rtype: None
    """
    return patient_service.get_patient_by_id(id)


def get_patients_ids():  # noqa: E501
    """Get patients ids

     # noqa: E501


    :rtype: None
    """
    return patient_service.get_patients()


def preview():
    file = patient_service.preview()
    return send_file(file, as_attachment=True, attachment_filename='temp.png', mimetype='image/png')
