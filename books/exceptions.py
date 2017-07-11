
from common_exceptions.exceptions import CommonBaseException


class MemberNotFoundError(CommonBaseException):
    error_code = 'memberNotFound'
    message = 'member Does not exist'

    def __init__(self):
        CommonBaseException.__init__(self, self.message, self.error_code)

