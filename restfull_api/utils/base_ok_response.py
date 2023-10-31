import json
from odoo.tools import date_utils
class BaseOkResponse:
    _name = 'base_ok_response'
    def __init__(self,message,data,statusCode = None):
      self.success = True 
      if statusCode == None: self.statusCode =200 
      else: self.statusCode = statusCode
      self.message = message
      self.data = data
    
    def toJSON(self):
        return json.dumps(self.__dict__, default= date_utils.json_default, 
            sort_keys=True, indent=4)