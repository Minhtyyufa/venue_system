class BaseError(Exception):
    def __init__(self, message):
        self.type = self.__class__.__name__
        self.message = message

class TestException(BaseError):
    pass

class InsufficientFields(BaseError):
    pass