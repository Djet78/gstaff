class BaseObjectResolverError(Exception):
    pass


class BadRequestError(BaseObjectResolverError):
    """ Raised when user passed non existing values to url. """
    pass


class NotFoundError(BaseObjectResolverError):
    """ Raised when Django model instance does not exist. """
    pass
