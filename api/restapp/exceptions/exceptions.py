
# Custom exception

from rest_framework.exceptions import APIException


class DolunayValidationError(APIException):
    status_code = 400
