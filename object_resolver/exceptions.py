class ObjectOperationError(Exception):
    pass


class BadRequestError(ObjectOperationError):
    pass


class NotFoundError(ObjectOperationError):
    pass
