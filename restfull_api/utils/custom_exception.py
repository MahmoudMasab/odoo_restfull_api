
from pyparsing import Any  

class InvalidJSONDataException(Exception):
    def __init__(self, message): 
        super().__init__(message)     
   
class ParamsErrorException(Exception):
       message:any