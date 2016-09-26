class ValidationError(Exception):
    def __init__(self, property_name, message):
        self._validation_set = None
        self._property_name = property_name
        self._message = message