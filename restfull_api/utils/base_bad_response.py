#from abc import ABCMeta, abstractmethod
#from interface import implements, Interface
from odoo.tools import date_utils
import json
class BaseBadResponse:
    def __init__(self,message,erorr = None,statusCode = None):
      self.success = False 
      if statusCode == None: self.statusCode = 400 
      else: self.statusCode = statusCode
      self.message = message
      self.erorr = erorr

    def toJSON(self):
        return json.dumps(self.__dict__, default= date_utils.json_default, 
            sort_keys=True, indent=4)  

 