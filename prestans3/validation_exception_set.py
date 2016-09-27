class ValidationExceptionSet(object):
    def __init__(self, namespace, validation_exception):
        """

        :param namespace:
        :param validation_exception:
         :type validation_exception: ``prestans3.errors.ValidationException``
        :param exceptionSet:
        """
        pass


class LeafException(object):
    def __init__(self, of_type, message=None):
        if message is None:
            self.message = DEFAULT_VALIDATION_MESSAGE
        self._of_type = of_type
        pass


DEFAULT_VALIDATION_MESSAGE = 'validation error'
