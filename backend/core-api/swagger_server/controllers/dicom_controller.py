import connexion
import six
import json

from swagger_server import util

# services
import swagger_server.services.patient_service as patient_service

from flask import send_file


def download_dicom(id):  # noqa: E501
    """Get patients ids

     # noqa: E501

    :param study: Studi id
    :type study: str

    :rtype: file
    """
    file = patient_service.get_dicom_media(id)
    return send_file(file, as_attachment=True, attachment_filename=id + '.dcm', mimetype='application/dicom')


def preview(id):
    decoded_string = patient_service.preview(id)
    return decoded_string