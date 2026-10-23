"""
Specific application exceptions.
"""


class MisslemonBaseException(Exception):
    """
    Exception base.

    You should never use it directly except for test purpose. Instead make or
    use a dedicated exception related to the error context.
    """
    pass


class AppOperationError(MisslemonBaseException):
    """
    Sample exception to raise from your code.
    """
    pass


class NoAvailableResource(MisslemonBaseException):
    """
    Exception to raise when Renamer does not find any resource to rename (ignored or
    identical status).
    """
    pass
