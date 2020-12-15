class BaseError(Exception):
    def __init__(self, message):
        self.type = self.__class__.__name__
        self.message = message

class TestException(BaseError):
    pass

class InsufficientFieldsException(BaseError):
    pass

class WrongAccountTypeException(BaseError):
    pass

class FieldTypeException(BaseError):
    pass

class DatabaseError(BaseError):
    pass

class TicketReservedAlreadyError(BaseError):
    pass