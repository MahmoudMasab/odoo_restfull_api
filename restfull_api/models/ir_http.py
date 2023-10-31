
import sys
from odoo import models
from odoo.http import request 
from odoo.tools import date_utils
from werkzeug.exceptions import Unauthorized,MethodNotAllowed
from ..utils.route_end_point import RouteEndPoint
from ..utils.base_bad_response import BaseBadResponse


class CustomHandleError(models.AbstractModel):
    _inherit = 'ir.http'

    # custom override _handle_error  of ir.http
    @classmethod
    def _handle_error(cls, exception):
        # chake custom response from api exception
        if(request.env.context.get('erorr_exception') != None):
            erorr_exception = request.env.context['erorr_exception'] 
            statusCode = request.env.context['statusCode']
            # delete key erorr_exception and statusCode from env.context
            dictkey = request.env.context
            del dictkey['erorr_exception']
            del dictkey['statusCode']
            request.env.context = dictkey
            # return custom response from api exception
            return request.make_response(erorr_exception, headers=[('Content-Type', 'application/json')], cookies=None, status = statusCode) 
        else:
          if RouteEndPoint.checkIsExitRouteEndPoint(routeEndPoint=request.httprequest.path):
                if isinstance(exception, Unauthorized):
                      return request.make_response(BaseBadResponse(message="Invalid to Unauthorized",erorr= sys.exc_info(),statusCode=401).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status = 401) 
                elif isinstance(exception,MethodNotAllowed):
                    return request.make_response(BaseBadResponse(message=exception,erorr= sys.exc_info(),statusCode=405).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status = 405) 
                else: return request.make_response(BaseBadResponse(message=exception,erorr= sys.exc_info()).toJSON(), headers=[('Content-Type', 'application/json')], cookies=None, status = 400) 
          else: return request.dispatcher.handle_error(exception)


 