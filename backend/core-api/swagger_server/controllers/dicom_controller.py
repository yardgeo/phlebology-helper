import connexion
import six

from swagger_server import util

# services
import swagger_server.services.patient_service as patient_service

from flask import send_file


def preview(study):  # noqa: E501
    """Get patients ids

     # noqa: E501

    :param study: Studi id
    :type study: str

    :rtype: file
    """
    file = patient_service.get_media(study)
    return send_file(file, as_attachment=True, attachment_filename='temp.zip', mimetype='application/zip')
