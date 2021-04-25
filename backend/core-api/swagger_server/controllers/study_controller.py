import connexion
import six

from swagger_server.models.study import Study  # noqa: E501
from swagger_server import util

# services
import swagger_server.services.patient_service as patient_service
import swagger_server.services.converter_service as converter_service


def get_study_by_id(studyId):  # noqa: E501
    """Get study by id

     # noqa: E501

    :param studyId: Study id
    :type studyId: str

    :rtype: Study
    """
    db_study = patient_service.get_study_by_id(studyId)
    return converter_service.study_to_model(db_study)
