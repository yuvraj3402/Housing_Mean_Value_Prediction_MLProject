import os,sys


class HousingException(Exception):
    def __init__(self,error_message:Exception,error_detail:sys):
        super().__init__(error_message)
        self.error_message=HousingException.get_detailed_error_message(error_message=error_message,
                                                                       error_detail=error_detail)



    @staticmethod
    def get_detailed_error_message(error_message:Exception,error_detail:sys):
 
        _,_,exec_tb=error_detail.exc_info()

        exec_block_number=exec_tb.tb_frame.f_lineno

        exec_line_number=exec_tb.tb_lineno

        exec_file_name=exec_tb.tb_frame.f_code.co_filename
        

        error_message=f"""error occured in file [{exec_file_name}] 
        at block  {[exec_block_number]} 
        in line number [{exec_line_number}]
        error message : [{error_message}]"""

        return error_message
    
    
    def __str__(self):
        return self.error_message


    def __repr__(self) -> str:
        return HousingException.__name__.str()
