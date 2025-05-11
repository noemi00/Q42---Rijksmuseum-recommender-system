from fastapi import HTTPException, status


class InternalServerError(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "An internal server error occured. {details}"

    def __init__(self, details):
        self.detail = self.detail.format(details=details)
        super(InternalServerError, self).__init__(
            detail=self.detail, status_code=self.status_code
        )


class BadGatewayException(HTTPException):
    status_code = status.HTTP_502_BAD_GATEWAY
    detail = "An error on a external server error occured. {details}"

    def __init__(self, details):
        self.detail = self.detail.format(details=details)
        super(BadGatewayException, self).__init__(
            detail=self.detail, status_code=self.status_code
        )


class ValidationException(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "The request was not according to semantic rules. {details}"

    def __init__(self, details):
        self.detail = self.detail.format(details=details)
        super(ValidationException, self).__init__(
            detail=self.detail, status_code=self.status_code
        )


class AuthenticationException(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "You are not authenticated for this operation. {details}"

    def __init__(self, details, headers=None):
        self.detail = self.detail.format(details=details)
        super(AuthenticationException, self).__init__(
            detail=self.detail, status_code=self.status_code, headers=headers
        )


class AuthorizationException(HTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "You are not authorized for this operation. {details}"

    def __init__(self, details):
        self.detail = self.detail.format(details=details)
        super(AuthorizationException, self).__init__(
            detail=self.detail, status_code=self.status_code
        )


class ResourceNotFoundException(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Cannot find {resource} identified by {identifier}."

    def __init__(self, resource, identifier):
        self.detail = self.detail.format(resource=resource, identifier=identifier)
        super(ResourceNotFoundException, self).__init__(
            detail=self.detail, status_code=self.status_code
        )
