import re
import time

import jwt

from odoo.http import request
secondsPerDay = 86400  
secondsPerMinute = 60
secondPerHour = 3600

accessTokenExpiresIn = secondsPerDay * 1 # number of days
refreshTokenExpiresIn =  (secondsPerDay * 1) + secondPerHour * 1 # number of hours
confirmCodeTokenExpiresIn = secondsPerMinute * 10   # number of Minutes
confirmResetExpiresIn = secondsPerMinute * 20   # number of Minutes

nameAccessToken = 'AccessToken'
nameRefreshToken = 'RefreshToken'
nameConfirmCodeToken = 'ConfirmCodeToken'
nameResetToken = 'ResetToken'

def check_data(data):
    return data if data else None


def check_and_remove_country_code_of_saudi_arabia(phone_number):
    keys = ['966', '+966', '00966','0']
    pattern = r'^(\+9665|9665|009665|5|05)?\d{8}$'
    if re.match(pattern, phone_number):
        for key in keys:
            if phone_number.startswith(key):
                digits = phone_number[len(key):]
                return digits
        return phone_number    
    else:
      return None

#get lang from header and update request env of Context
def fetchRequestLanguage():
      lang = request.httprequest.headers.get('lang')
      dictkey = request.env.context
      if(lang == None):
        dictkey = dict(dictkey,lang= 'en_US')
      elif(lang.startswith("ar")):

        dictkey = dict(dictkey,lang= 'ar_001') 
      else:
        dictkey = dict(dictkey,lang= 'en_US') 
      request.env.context = dictkey
 
 # create Token
def create_tokenSiginApple():
      private_key = """-----BEGIN PRIVATE KEY-----
MIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHkwdwIBAQQgoU9cr8eeiwK1PmZu
3C6FkRy7eL0X9miDWyyVh2+ykYegCgYIKoZIzj0DAQehRANCAAR3Dyv8U2nWzwwf
yAu4jKREQ0sxmsPaSNnqMdXhNgqqITT/A5sL6vVz77eeyAD+ujo+bi0mMDRYfz9H
QkZkNelz
-----END PRIVATE KEY-----"""
      payload = {
    "iss": "D699SS3X8T",
    "iat": time.time(),
    "exp": time.time() + (secondsPerDay * 180),
    "aud": "https://appleid.apple.com",
    "sub": "Roqay.com.QuranShaby"
     }
      print('token')
      access_token = jwt.encode(
         payload, private_key, algorithm='ES256', headers= {"kid": "M4QGC6234"}
      )
      return access_token 
#  # create Token
# def create_tokenSiginApple():
#       private_key = """-----BEGIN PRIVATE KEY-----
# MIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHkwdwIBAQQgz4EkuXqjvkPpfdZJ
# ZvJpZSwLwPfWKGfAOZZa7XXio/+gCgYIKoZIzj0DAQehRANCAASCxt3pBAMJjsWz
# 013gf+Eb/3NY/gzPD87ipeOpSd8vZBDG16yNR7tjUv68trYuMYSZZ9V6cCy1On5Z
# 5nq6KiE5
# -----END PRIVATE KEY-----"""
#       payload = {
#     "iss": "ML37J3DA4L",
#     "iat": time.time(),
#     "exp": time.time() + (secondsPerDay * 180),
#     "aud": "https://appleid.apple.com",
#     "sub": "com.example.siginApple"
#      }
#       print('token')
#       access_token = jwt.encode(
#          payload, private_key, algorithm='ES256', headers= {"kid": "M4QGC6234V"}
#       )
#       return access_token 

 # create Token
def create_token(validator,expiresIn, aud=None, email=None, partner_id=None):
      payload = {
            'aud': aud or validator.audience,
            'iss': validator.issuer,
            'exp': time.time() + expiresIn,
      }
      if email:
          payload['email'] = email
      if partner_id:
          payload['id'] = partner_id
      access_token = jwt.encode(
         payload, key=validator.secret_key, algorithm=validator.secret_algorithm
      )
      return access_token 
# get lValidator PortalAuth
def getValidatorPortalAuth():
      portal_auth = request.env['auth.jwt.validator'].sudo().search([('name', '=', 'portal_auth')])
      if not portal_auth:
          request.env['auth.jwt.validator'].sudo().create(
            dict(
                name="portal_auth",
                signature_type="secret",
                secret_algorithm="HS256",
                secret_key="self-service-key",
                audience='auth_jwt_portal_api',
                issuer="portal issuer",
                user_id_strategy="static",
                static_user_id=1,
                partner_id_strategy="id",
                partner_id_required=True,
            ))
          return request.env['auth.jwt.validator'].sudo().search([('name', '=', 'portal_auth')])
      return request.env['auth.jwt.validator'].sudo().search([('name', '=', 'portal_auth')])
# get lValidator PortalAuth
def getValidatorRefreshAuth():
      refresh_auth = request.env['auth.jwt.validator'].sudo().search([('name', '=', 'refresh_auth')])
      if not refresh_auth:
          request.env['auth.jwt.validator'].sudo().create(
            dict(
                name="refresh_auth",
                signature_type="secret",
                secret_algorithm="HS256",
                secret_key="self-service-key",
                audience='auth_jwt_refresh_api',
                issuer="refresh issuer",
                user_id_strategy="static",
                static_user_id=1,
                partner_id_strategy="id",
                partner_id_required=True,
            ))
          return request.env['auth.jwt.validator'].sudo().search([('name', '=', 'refresh_auth')])
      return request.env['auth.jwt.validator'].sudo().search([('name', '=', 'refresh_auth')])
# get lValidator PortalAuth
def getValidatorConfirmAuth():
      confirm_auth = request.env['auth.jwt.validator'].sudo().search([('name', '=', 'confirm_auth')])
      if not confirm_auth:
          request.env['auth.jwt.validator'].sudo().create(
            dict(
                name="confirm_auth",
                signature_type="secret",
                secret_algorithm="HS256",
                secret_key="self-service-key",
                audience='auth_jwt_confirm_api',
                issuer="confirm issuer",
                user_id_strategy="static",
                static_user_id=1,
                partner_id_strategy="id",
                partner_id_required=True,
            ))
          return request.env['auth.jwt.validator'].sudo().search([('name', '=', 'confirm_auth')])
      return request.env['auth.jwt.validator'].sudo().search([('name', '=', 'confirm_auth')])
# get lValidator PortalAuth
def getValidatorResetAuth():
      rest_auth = request.env['auth.jwt.validator'].sudo().search([('name', '=', 'reset_auth')])
      if not rest_auth:
          request.env['auth.jwt.validator'].sudo().create(
            dict(
                name="reset_auth",
                signature_type="secret",
                secret_algorithm="HS256",
                secret_key="self-service-key",
                audience='auth_jwt_rest_api',
                issuer="Rest issuer",
                user_id_strategy="static",
                static_user_id=1,
                partner_id_strategy="id",
                partner_id_required=True,
            ))
          return request.env['auth.jwt.validator'].sudo().search([('name', '=', 'reset_auth')])
      return rest_auth
      