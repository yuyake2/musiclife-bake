class BusinessError(Exception):

    error_code = 0
    error_msg = None

    def __init__(self, error_code, error_msg=None):
        self.error_code = error_code
        self.error_msg = error_msg
        super(BusinessError,self).__init__(self.get_error_msg())

    def get_error_msg(self):
        if self.error_msg is not None:
            return self.error_msg

        return ERROR_MSG.get(self.error_code)
