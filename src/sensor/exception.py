import sys

def error_msg_details(error, errorDetail:sys):
    _,_,exc_tb = errorDetail.exc_info()
    fileName = exc_tb.tb_frame.f_code.co_filename
    lineNo = exc_tb.tb_lineno
    errorMsg = "Error occured python script name [{0}] line number [{1}] error msg [{2}]".format(
        fileName,lineNo, str(error)
        )
    return errorMsg

class CustomException(Exception):

    def __init__(self, errorMsg, errorDetail:sys):
        self.errorMsg = error_msg_details(error=errorMsg, errorDetail=errorDetail)


    def __str__(self):
        return self.errorMsg