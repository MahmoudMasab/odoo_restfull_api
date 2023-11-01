import json

from ..utils.route_end_point import RouteEndPoint
from ..utils.exceptions_unauthorized import UnauthorizedInvalidToken, UnauthorizedMissingAuthorizationHeader
from odoo import exceptions,_
import sys
from ..service.auth_service import IAuthService  
from odoo import http
from odoo.http import request
from ..utils.base_ok_response import BaseOkResponse
from ..utils.base_bad_response import BaseBadResponse
from ..utils.custom_exception import  ParamsErrorException 
from ..service.dependency_container import dependency_container 


class AuthController(http.Controller):
    authService: IAuthService = None
    def __init__(self):
         self.authService = dependency_container.get_dependency(IAuthService)
    
    @http.route(RouteEndPoint.signUp, method=['POST'], auth='public', csrf=False, cors='*')
    def signUp(self, **kwargs):
      print('signUp')
      try:  
           result = self.authService.signUp()
           return request.make_response(BaseOkResponse(message=_("success signUp"),data=result).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=200)
      except json.decoder.JSONDecodeError as error:    
            return request.make_response(BaseBadResponse(message=_("invalid json data"),erorr= sys.exc_info()).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=400)
      except ParamsErrorException as error:
            return request.make_response(BaseBadResponse(message=error,erorr= sys.exc_info()).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=400)
      except exceptions.AccessDenied as error:
            return request.make_response(BaseBadResponse(message=_('password erorr'),erorr= sys.exc_info()).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=400)
      except exceptions.ValidationError as e:
            request.env.context = dict(request.env.context, erorr_exception = BaseBadResponse(message=e,erorr= sys.exc_info()[0]).toJSON(),statusCode= 400)
            pass
      except:
            request.env.context = dict(request.env.context, erorr_exception = BaseBadResponse(message=_("unexpected error"),erorr= sys.exc_info()[0]).toJSON(),statusCode= 400)
            return request.make_response(BaseBadResponse(message=_("unexpected error"),erorr= sys.exc_info()).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=400)
     
    @http.route(RouteEndPoint.signIn, method=['POST'], auth='public', csrf=False, cors='*')
    def signIn(self, **kwargs):
      print('signIn')
      try: 
           result = self.authService.signIn()
           return request.make_response(BaseOkResponse(message=_("success login"),data=result).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=200)
      except json.decoder.JSONDecodeError as error:    
            return request.make_response(BaseBadResponse(message=_("invalid json data"),erorr= sys.exc_info()).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=400)
      except ParamsErrorException as error:
            return request.make_response(BaseBadResponse(message=error,erorr= sys.exc_info()).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=400)
      except exceptions.AccessDenied as error:
            return request.make_response(BaseBadResponse(message=_('password erorr'),erorr= sys.exc_info()).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=400)
      except exceptions.ValidationError as e:
            request.env.context = dict(request.env.context, erorr_exception = BaseBadResponse(message=e,erorr= sys.exc_info()[0]).toJSON(),statusCode= 400)
            pass
      except:
            request.env.context = dict(request.env.context, erorr_exception = BaseBadResponse(message=_("unexpected error"),erorr= sys.exc_info()[0]).toJSON(),statusCode= 400)
            return request.make_response(BaseBadResponse(message=_("unexpected error"),erorr= sys.exc_info()).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=400)
     
    @http.route(RouteEndPoint.logout, method=['POST'], auth='jwt_portal_auth', csrf=False, cors='*')
    def logout(self, **kwargs):
      print('logout')
      try: 
           self.authService.validatorToken()
           self.authService.logout()
           return request.make_response(BaseOkResponse(message=_("success_logout"),data=None).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=200)  
      except UnauthorizedInvalidToken:    
            return request.make_response(BaseBadResponse(message=_("invalid token"),erorr= sys.exc_info(),statusCode=401).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=401)
      except UnauthorizedMissingAuthorizationHeader:    
            return request.make_response(BaseBadResponse(message=_("token missing"),erorr= sys.exc_info(),statusCode=401).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=401)
      except:
            request.env.context = dict(request.env.context, erorr_exception = BaseBadResponse(message=_("unexpected error"),erorr= sys.exc_info()[0]).toJSON(),statusCode= 400)
            return request.make_response(BaseBadResponse(message=_("unexpected error"),erorr= sys.exc_info()).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=400)
    
    
    @http.route(RouteEndPoint.logoutAllDevice, method=['POST'], auth='jwt_portal_auth', csrf=False, cors='*')
    def logoutAllDevice(self, **kwargs):
      print('logoutAllDevice')
      try: 
           self.authService.validatorToken()
           self.authService.logoutAllDevice()
           return request.make_response(BaseOkResponse(message=_("success_logout_all_device"),data=None).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=200)  
      except UnauthorizedInvalidToken:    
            return request.make_response(BaseBadResponse(message=_("invalid token"),erorr= sys.exc_info(),statusCode=401).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=401)
      except UnauthorizedMissingAuthorizationHeader:    
            return request.make_response(BaseBadResponse(message=_("token missing"),erorr= sys.exc_info(),statusCode=401).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=401)
      except:
            request.env.context = dict(request.env.context, erorr_exception = BaseBadResponse(message=_("unexpected error"),erorr= sys.exc_info()[0]).toJSON(),statusCode= 400)
            return request.make_response(BaseBadResponse(message=_("unexpected error"),erorr= sys.exc_info()).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=400)
    
    @http.route(RouteEndPoint.refreshToken, method=['POST'], auth='jwt_refresh_auth', csrf=False, cors='*')
    def refreshToken(self, **kwargs):
      print('logout')
      try: 
           self.authService.validatorRefreshToken()
           result = self.authService.refreshToken()
           return request.make_response(BaseOkResponse(message="ok",data=result).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=200)  
      except UnauthorizedInvalidToken:    
            return request.make_response(BaseBadResponse(message=_("invalid token"),erorr= sys.exc_info(),statusCode=401).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=401)
      except UnauthorizedMissingAuthorizationHeader:    
            return request.make_response(BaseBadResponse(message=_("token missing"),erorr= sys.exc_info(),statusCode=401).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=401)
      except:
            request.env.context = dict(request.env.context, erorr_exception = BaseBadResponse(message=_("unexpected error"),erorr= sys.exc_info()[0]).toJSON(),statusCode= 400)
            return request.make_response(BaseBadResponse(message=_("unexpected error"),erorr= sys.exc_info()).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=400)
    
    
    @http.route(RouteEndPoint.sendCode, method=['POST'], auth='public', csrf=False, cors='*')
    def sendCode(self, **kwargs):
      print('sendCode')
      try:
        result = self.authService.sendCode() 
        return request.make_response(BaseOkResponse(message=_("the_code_has_send"),data=result).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=200)
      except json.decoder.JSONDecodeError as error:    
            return request.make_response(BaseBadResponse(message=_("invalid json data"),erorr= error).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=400)
      except ParamsErrorException as error:
            print(error)   
            return request.make_response(BaseBadResponse(message=error,erorr= sys.exc_info()).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=400)
      except exceptions.ValidationError as e:
            request.env.context = dict(request.env.context, erorr_exception = BaseBadResponse(message=e,erorr= sys.exc_info()[0]).toJSON(),statusCode= 400)
            pass
      except:
            request.env.context = dict(request.env.context, erorr_exception = BaseBadResponse(message=_("unexpected error"),erorr= sys.exc_info()[0]).toJSON(),statusCode= 400)
            return request.make_response(BaseBadResponse(message=_("unexpected error"),erorr= sys.exc_info()).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=400)
    
    
    @http.route(RouteEndPoint.registerConfirmCode, method=['POST'], auth='jwt_confirm_auth', csrf=False, cors='*')
    def confirmCode(self, **kwargs):
      print('confirmCode')
      try:
        self.authService.validatorConfirmToken()
        result = self.authService.confirmCode() 
        return request.make_response(BaseOkResponse(message="ok",data=result).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=200)
      except json.decoder.JSONDecodeError as error:    
            return request.make_response(BaseBadResponse(message=_("invalid json data"),erorr= error).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=400)
      except UnauthorizedInvalidToken:    
            return request.make_response(BaseBadResponse(message=_("invalid token"),erorr= sys.exc_info(),statusCode=401).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=401)
      except UnauthorizedMissingAuthorizationHeader:    
            return request.make_response(BaseBadResponse(message=_("token missing"),erorr= sys.exc_info(),statusCode=401).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=401)
      except ParamsErrorException as error:
            print(error)   
            return request.make_response(BaseBadResponse(message=error,erorr= sys.exc_info()).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=400)
      except exceptions.ValidationError as e:
            request.env.context = dict(request.env.context, erorr_exception = BaseBadResponse(message=e,erorr= sys.exc_info()[0]).toJSON(),statusCode= 400)
            pass
      except:
            request.env.context = dict(request.env.context, erorr_exception = BaseBadResponse(message=_("unexpected error"),erorr= sys.exc_info()[0]).toJSON(),statusCode= 400)
            return request.make_response(BaseBadResponse(message=_("unexpected error"),erorr= sys.exc_info()).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=400)
   
   
    @http.route(RouteEndPoint.confirmResetPassword, method=['POST'], auth='jwt_confirm_auth', csrf=False, cors='*')
    def confirmResetPassword(self, **kwargs):
      print('confirmCode')
      try:
        self.authService.validatorConfirmToken()
        result = self.authService.confirmResetPassword() 
        return request.make_response(BaseOkResponse(message="ok",data=result).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=200)
      except json.decoder.JSONDecodeError as error:    
            return request.make_response(BaseBadResponse(message=_("invalid json data"),erorr= error).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=400)
      except UnauthorizedInvalidToken:    
            return request.make_response(BaseBadResponse(message=_("invalid token"),erorr= sys.exc_info(),statusCode=401).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=401)
      except UnauthorizedMissingAuthorizationHeader:    
            return request.make_response(BaseBadResponse(message=_("token missing"),erorr= sys.exc_info(),statusCode=401).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=401)
      except ParamsErrorException as error:
            print(error)   
            return request.make_response(BaseBadResponse(message=error,erorr= sys.exc_info()).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=400)
      except exceptions.ValidationError as e:
            request.env.context = dict(request.env.context, erorr_exception = BaseBadResponse(message=e,erorr= sys.exc_info()[0]).toJSON(),statusCode= 400)
            pass
      except:
            request.env.context = dict(request.env.context, erorr_exception = BaseBadResponse(message=_("unexpected error"),erorr= sys.exc_info()[0]).toJSON(),statusCode= 400)
            return request.make_response(BaseBadResponse(message=_("unexpected error"),erorr= sys.exc_info()).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=400)

 
    @http.route(RouteEndPoint.changePassword, method=['POST'], auth='jwt_reset_auth', csrf=False, cors='*')
    def changePassword(self, **kwargs):
      print('changePassword')
      try:
        self.authService.validatorResetToken()
        result = self.authService.changePassword() 
        return request.make_response(BaseOkResponse(message="ok",data=result).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=200)
      except json.decoder.JSONDecodeError as error:    
            return request.make_response(BaseBadResponse(message=_("invalid json data"),erorr= sys.exc_info()).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=400)
      except UnauthorizedInvalidToken:    
            return request.make_response(BaseBadResponse(message=_("invalid token"),erorr= sys.exc_info(),statusCode=401).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=401)
      except UnauthorizedMissingAuthorizationHeader:    
            return request.make_response(BaseBadResponse(message=_("token missing"),erorr= sys.exc_info(),statusCode=401).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=401)
      except ParamsErrorException as error:
            print(error)   
            return request.make_response(BaseBadResponse(message=error,erorr= sys.exc_info()).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=400)
      except exceptions.ValidationError as e:
            request.env.context = dict(request.env.context, erorr_exception = BaseBadResponse(message=e,erorr= sys.exc_info()[0]).toJSON(),statusCode= 400)
            pass
      except:
            request.env.context = dict(request.env.context, erorr_exception = BaseBadResponse(message=_("unexpected error"),erorr= sys.exc_info()[0]).toJSON(),statusCode= 400)
            return request.make_response(BaseBadResponse(message=_("unexpected error"),erorr= sys.exc_info()).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status=400)

 