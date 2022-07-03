__all__ = ["LoginError", "RequestError", "PostError"]


class LoginError(Exception):
    pass


class RequestError(Exception):
    pass


class PostError(Exception):
    pass
