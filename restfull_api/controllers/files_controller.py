import base64
from odoo import http
from odoo.http import request
from odoo.tools import  file_open
import werkzeug 
from odoo.tools.mimetypes import guess_mimetype
class FilesController(http.Controller):

    @http.route('/.well-known/apple-app-site-association', type='http', auth='public')
    def fileAppleAppSiteAssociation(self):
        file_path = 'restfull_api/static/json/apple-app-site-association'
        with file_open(file_path, 'rb') as file:
            file_contents = file.read()

        file_data = base64.b64encode(file_contents) 
        mimetype = guess_mimetype(file_data)
        response = werkzeug.wrappers.Response()
        response.make_conditional(request.httprequest)
        if response.status_code == 304:
                return response
        response.mimetype = mimetype
        response.data = base64.b64decode(file_data)
        return response
    
    @http.route('/.well-known/apple-developer-merchantid-domain-association.txt', type='http', auth='public')
    def fileAppleDeveloperMerchantidDomainAssociation(self):
        file_path = 'restfull_api/static/src/apple-developer-merchantid-domain-association.txt'
        with file_open(file_path, 'rb') as file:
            file_contents = file.read()

        file_data = base64.b64encode(file_contents) 
        mimetype = guess_mimetype(file_data)
        response = werkzeug.wrappers.Response()
        response.make_conditional(request.httprequest)
        if response.status_code == 304:
                return response
        response.mimetype = mimetype
        response.data = base64.b64decode(file_data)
        return response
