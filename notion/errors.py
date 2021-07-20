from enum import Enum
from typing import Optional

from httpx import Headers, Response


class APIErrorCode(str, Enum):
    UNAUTHORIZED = "unauthorized"
    RESTRICTED_RESOURCE = "restricted_resource"
    OBJECT_NOT_FOUND = "object_not_found"
    RATE_LIMITED = "rate_limited"
    INVALID_JSON = "invalid_json"
    INVALID_REQUEST_URL = "invalid_request_url"
    INVALID_REQUEST = "invalid_request"
    VALIDATION_ERROR = "validation_error"
    CONFLICT_ERROR = "conflict_error"
    INTERNAL_SERVER_ERROR = "internal_server_error"
    SERVICE_UNAVAILABLE = "service_unavailable"


class ClientErrorCode(str, Enum):
    REQUEST_TIMEOUT = "notionhq_client_request_timeout"
    RESPONSE_ERROR = "notionhq_client_response_error"


class RequestTimeoutError(Exception):
    code: ClientErrorCode = ClientErrorCode.REQUEST_TIMEOUT

    def __init__(self, message: str = "Request to Notion API has timed out") -> None:
        super().__init__(message)


class HTTPResponseError(Exception):
    code: ClientErrorCode = ClientErrorCode.RESPONSE_ERROR
    status: int
    headers: Headers
    body: str

    def __init__(self, response: Response, msg: Optional[str] = None) -> None:
        super().__init__(msg)
        self.status = response.status_code
        self.headers = response.headers
        self.body = response.text


class APIResponseError(HTTPResponseError):
    code: APIErrorCode

    def __init__(self, response: Response, msg: str, code: APIErrorCode) -> None:
        super().__init__(response, msg=msg)
        self.code = code


def is_api_error(code: str) -> bool:
    return isinstance(code, str) and code in (error.value for error in APIErrorCode)
