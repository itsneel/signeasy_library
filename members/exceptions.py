
from common_exceptions.exceptions import CommonBaseException


class SkuNotpresetError(CommonBaseException):
    error_code = 'skuNotpreset'
    message = 'Sku is not sent'

    def __init__(self):
        CommonBaseException.__init__(self, self.message, self.error_code)


class BookNotFoundError(CommonBaseException):
    error_code = 'bookNotFound'
    message = 'Select Book Does not exist'

    def __init__(self):
        CommonBaseException.__init__(self, self.message, self.error_code)


class BookCanNotBeIssuedError(CommonBaseException):
    error_code = 'bookCanNotBeIssuedError'
    message = 'Selected Book is not avaialble to issue'

    def __init__(self):
        CommonBaseException.__init__(self, self.message, self.error_code)
