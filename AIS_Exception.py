# class for exception
#Could be improve
class AIS_Exception(Exception):
    """ Exception class, just print a message """
    def __init__(self, message) -> None:
        self.message = message