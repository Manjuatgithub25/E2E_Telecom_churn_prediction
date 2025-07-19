import sys

def error_message_details(error, error_details:sys):
    _, _, exc_table = error_details.exc_info()
    file_name = exc_table.tb_frame.f_code.co_filename
    line_no = exc_table.tb_lineno
    error_message = "The error is occured in python file {0} at line number {1}: that is {2}".format(file_name, line_no, str(error))
    return error_message


class CustomException(Exception):
    def __init__(self, error_message, error_details:sys):
        super().__init__(error_message)
        self.error_message = error_message_details(error_message, error_details=error_details)

    
    def __str__(self):
        return self.error_message