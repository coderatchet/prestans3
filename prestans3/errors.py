class ValidationException(Exception):
    def __init__(self, message):
        self._validation_set = None
        self._message = message