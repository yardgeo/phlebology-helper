import connexion
import six

from swagger_server.models.series import Series  # noqa: E501
from swagger_server import util


# services
import swagger_server.services.patient_service as patient_service
import swagger_server.services.converter_service as converter_service


def get_series_by_id(seriesId):  # noqa: E501
    """Get series by id

     # noqa: E501

    :param seriesId: series id
    :type seriesId: str

    :rtype: Series
    """
    db_series = patient_service.get_series_by_id(seriesId)
    return converter_service.series_to_model(db_series)


def get_state(seriesId):  # noqa: E501
    """Get series state

     # noqa: E501

    :param seriesId: Series id
    :type seriesId: str

    :rtype: object
    """
    state = patient_service.get_original_state(seriesId)
    return state


def upload_state(seriesId, state):  # noqa: E501
    """Upload series state

     # noqa: E501

    :param seriesId: Series id
    :type seriesId: str
    :param state: State
    :type state: 

    :rtype: None
    """
    patient_service.upload_original_state(series_id=seriesId, state=state)
    return 'Ok!'
