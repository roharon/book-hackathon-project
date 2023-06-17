class BadRequestException(Exception):
    def __init__(self, message: str):
        self.status_code = 400
        self.message = message


class NotFoundException(Exception):
    def __init__(self, message: str):
        self.status_code = 404
        self.message = message
