class RequestFileError(Exception):
    def __init__(self, message=""):
        self.message = message


class DuplicateNameError(RequestFileError):
    def __init__(self, message=""):
        super().__init__(message)


class ParserNotFoundError(RequestFileError):
    def __init__(self, message=""):
        super().__init__(message)


class ValidateError(RequestFileError):
    def __init__(self, message=""):
        super().__init__(message)
