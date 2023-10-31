


from ..utils.exceptions_unauthorized import UnauthorizedInvalidToken, UnauthorizedMissingAuthorizationHeader
from ..models.users_token import UsersToken
from ..utils.response_models.user_auth_response import UserAuthResponce
from odoo.http import request
from ..utils.custom_exception import ParamsErrorException

from ..utils.methods_constants import check_data, check_and_remove_country_code_of_saudi_arabia,fetchRequestLanguage, getValidatorConfirmAuth,getValidatorPortalAuth,accessTokenExpiresIn, getValidatorRefreshAuth, getValidatorResetAuth,refreshTokenExpiresIn,confirmCodeTokenExpiresIn,nameAccessToken,nameRefreshToken,nameConfirmCodeToken,confirmResetExpiresIn,nameResetToken,create_token

from ..utils.models_name import ModelsName
from odoo import _

class AuthRepository:
    @staticmethod
    def signUp():
            fetchRequestLanguage()
            args =  request.get_json_data()
            required_fields=['name','country_id','mobile', 'password']
            if not any(field not in args.keys() for field in required_fields):
              login = str(args.get('mobile'))
              phone_number = check_and_remove_country_code_of_saudi_arabia(login)
              password = str(args.get('password'))
              name = str(args.get('name'))
              # Create a user
              user_sudo = request.env[ModelsName.usersRES].sudo().create({
                  'name': name,
                  'login': phone_number,
                  'password': password,
              })
              # add user detiles 
              user_sudo.partner_id.sudo().write({
               'name':name, 
               'email': str(args.get('email', None)),
               'country_id':str(args.get('country_id')),
               'mobile': phone_number
              })  
               
              user_sudo.sudo().random_confirmation_code()
              print("confirmation_code :",user_sudo.confirmation_code)
              validatorConfirmAuth = getValidatorConfirmAuth()
              confirmToken = create_token(validatorConfirmAuth,expiresIn= refreshTokenExpiresIn, partner_id=user_sudo.partner_id.id)
              request.env[ModelsName.matlobUsersTokens].sudo().create(
                        UsersToken.toMap(token=confirmToken,refresh_token=None ,type=nameConfirmCodeToken ,user_id=user_sudo.id)
              ) 
              return {"confirm_token": confirmToken}   
            else: raise ParamsErrorException("the fields name,mobile,country_id or password are not found in json bady")

    @staticmethod
    def signIn():
            fetchRequestLanguage()
            validatorPortalAuth = getValidatorPortalAuth()
            validatorRefreshAuth = getValidatorRefreshAuth()
            args =  request.get_json_data()
            if 'login' in args and 'password' in args:
              login = str(args.get('login'))
              phone_number = check_and_remove_country_code_of_saudi_arabia(login)
              password = str(args.get('password'))
              user_sudo = None;
              # get user 
              if phone_number != None :
                 user_sudo = request.env[ModelsName.usersRES].sudo().search(
                    [('login', '=', phone_number)], limit=1)
              else:     
                 user_sudo = request.env[ModelsName.usersRES].sudo().search(
                    [('name', '=', phone_number)], limit=1)
                 
              # check user  
              if user_sudo:
                    user_sudo.check(request.session.db , uid=user_sudo.id,passwd= password)
                    accessToken = create_token(validatorPortalAuth,expiresIn= accessTokenExpiresIn, partner_id=user_sudo.partner_id.id)
                    refreshToken = create_token(validatorRefreshAuth,expiresIn= refreshTokenExpiresIn, partner_id=user_sudo.partner_id.id)
                    request.env[ModelsName.matlobUsersTokens].sudo().create(
                        UsersToken.toMap(token=accessToken,refresh_token=refreshToken ,type=nameAccessToken ,user_id=user_sudo.id)
                    )
                    user_responce = UserAuthResponce(
                        id = user_sudo.id,
                        name = check_data(user_sudo.name),
                        email= check_data(user_sudo.email),
                        company_id = user_sudo.company_id.id,
                        company_name = check_data(user_sudo.company_id.name),
                        access_token = accessToken,
                        refresh_token = refreshToken,
                        is_complete = user_sudo.is_complete
                        )
                    return vars(user_responce)  
              else: 
                   raise ParamsErrorException("user_not_found")
            else: raise ParamsErrorException("the key login or password are not found in json bady")



    @staticmethod
    def logout():
        fetchRequestLanguage()
        token = request.env["ir.http"]._get_bearer_token()
        user_token = request.env[ModelsName.matlobUsersTokens].sudo().search(
                    [('token', '=', token)], limit=1)
        user_token.revoked_token()
        pass

    @staticmethod
    def logoutAllDevice():
        fetchRequestLanguage()
        user_sudo = request.env[ModelsName.usersRES].sudo().search(
                    [('partner_id', '=', request.jwt_partner_id)], limit=1)
        user_tokens = request.env[ModelsName.matlobUsersTokens].sudo().search(
                    [('user_id', '=', user_sudo.id)])
        print(user_tokens)
        if user_tokens:
           user_tokens.mapped(lambda user_token: user_token.revoked_token())
        pass  
    
    @staticmethod
    def sendCode():
            fetchRequestLanguage()
            args =  request.get_json_data()
            if 'number' in args:
              phone_number = check_and_remove_country_code_of_saudi_arabia(str(args.get('number')))
              if phone_number == None :
                   raise ParamsErrorException("the number is incorrect")
              # number correct
              user_sudo = request.env[ModelsName.usersRES].sudo().search(
                    [('login', '=', phone_number)], limit=1)
              if user_sudo:
                     user_sudo.sudo().random_confirmation_code()
                     #add Service confirmation_code
                     print("confirmation_code :",user_sudo.confirmation_code)
                     validatorConfirmAuth = getValidatorConfirmAuth()
                     confirmToken = create_token(validatorConfirmAuth,expiresIn= refreshTokenExpiresIn, partner_id=user_sudo.partner_id.id)
                     request.env[ModelsName.matlobUsersTokens].sudo().create(
                        UsersToken.toMap(token=confirmToken,refresh_token=None ,type=nameConfirmCodeToken ,user_id=user_sudo.id)
                     )
                     return {"confirm_token": confirmToken}  
              else: raise ParamsErrorException("the number is not found")
            else: raise ParamsErrorException("the key number is not found json")  
    
    @staticmethod
    def validatorToken():
        fetchRequestLanguage()
        token = request.env["ir.http"]._get_bearer_token()
        user_token = request.env[ModelsName.matlobUsersTokens].sudo().search(
                    [('token', '=', token)], limit=1)
        if not user_token:
             raise UnauthorizedInvalidToken
        elif user_token.revoked:
             raise UnauthorizedMissingAuthorizationHeader
        else: 'ok'

    @staticmethod
    def validatorRefreshToken():
        fetchRequestLanguage()
        token = request.env["ir.http"]._get_bearer_token()
        user_token = request.env[ModelsName.matlobUsersTokens].sudo().search(
                    [('refresh_token', '=', token)], limit=1)
        if not user_token:
             raise UnauthorizedInvalidToken
        elif user_token.revoked:
             raise UnauthorizedMissingAuthorizationHeader
        else: 'ok'

    @staticmethod
    def validatorConfirmToken():
        fetchRequestLanguage()
        token = request.env["ir.http"]._get_bearer_token()
        user_token = request.env[ModelsName.matlobUsersTokens].sudo().search(
                    [('token', '=', token)], limit=1)
        if not user_token:
             raise UnauthorizedInvalidToken
        elif user_token.revoked:
             raise UnauthorizedMissingAuthorizationHeader
        else: 'ok'

    @staticmethod
    def validatorResetToken():
        fetchRequestLanguage()
        token = request.env["ir.http"]._get_bearer_token()
        user_token = request.env[ModelsName.matlobUsersTokens].sudo().search(
                    [('token', '=', token)], limit=1)
        if not user_token:
             raise UnauthorizedInvalidToken
        elif user_token.revoked:
             raise UnauthorizedMissingAuthorizationHeader
        else: 'ok'

    @staticmethod
    def refreshToken():
        fetchRequestLanguage()
        user_sudo = request.env[ModelsName.usersRES].sudo().search(
                    [('partner_id', '=', request.jwt_partner_id)], limit=1)
        validatorPortalAuth = getValidatorPortalAuth()
        accessToken = create_token(validatorPortalAuth,expiresIn= accessTokenExpiresIn, partner_id=user_sudo.partner_id.id)
        
        token = request.env["ir.http"]._get_bearer_token()
        user_token = request.env[ModelsName.matlobUsersTokens].sudo().search(
                    [('refresh_token', '=', token)], limit=1)
        user_token.update_token(token=accessToken)
        return {"access_token": accessToken }
    
    @staticmethod
    def confirmResetPassword():
        fetchRequestLanguage()
        args =  request.get_json_data()
        if 'confirmation_code' in args:
          confirmation_code = int(args.get('confirmation_code'))
          user_sudo = request.env[ModelsName.usersRES].sudo().search(
                    [('partner_id', '=', request.jwt_partner_id)], limit=1)
          if user_sudo:
                 if user_sudo.confirmation_code == confirmation_code:      
                     validatorResetAuth = getValidatorResetAuth()
                     confirmResetToken = create_token(validatorResetAuth,expiresIn= confirmResetExpiresIn, partner_id=user_sudo.partner_id.id)
                     request.env[ModelsName.matlobUsersTokens].sudo().create(
                        UsersToken.toMap(token=confirmResetToken,refresh_token=None ,type=nameResetToken ,user_id=user_sudo.id)
                      )
                 else:  
                   raise ParamsErrorException("confirmation code is not equal")
          else: 
               raise ParamsErrorException("user_not_found")
           
          return {"confirm_reset_token": confirmResetToken }
        else: raise ParamsErrorException("the key confirmation code isnot found in json bady")
        

    @staticmethod
    def confirmCode():
        fetchRequestLanguage()
        args =  request.get_json_data()
        if 'confirmation_code' in args:
            confirmation_code = int(args.get('confirmation_code'))
            user_sudo = request.env[ModelsName.usersRES].sudo().search(
                    [('partner_id', '=', request.jwt_partner_id)], limit=1)
            if  user_sudo:
                if not user_sudo.is_complete:
                 if user_sudo.confirmation_code == confirmation_code:
                    user_sudo.sudo().write({
                    "active": True,
                    "is_complete": True
                    })
                    #revoked_token 
                    token = request.env["ir.http"]._get_bearer_token()
                    user_confirmToken = request.env[ModelsName.matlobUsersTokens].sudo().search(
                    [('token', '=', token)], limit=1)
                    user_confirmToken.revoked_token()
                    # get validator Tokens
                    validatorPortalAuth = getValidatorPortalAuth()
                    validatorRefreshAuth = getValidatorRefreshAuth()
                    # create Tokens and save in UsersTokens
                    accessToken = create_token(validatorPortalAuth,expiresIn= accessTokenExpiresIn, partner_id=user_sudo.partner_id.id)
                    refreshToken = create_token(validatorRefreshAuth,expiresIn= refreshTokenExpiresIn, partner_id=user_sudo.partner_id.id)
                    request.env[ModelsName.matlobUsersTokens].sudo().create(
                        UsersToken.toMap(token=accessToken,refresh_token=refreshToken ,type=nameAccessToken ,user_id=user_sudo.id)
                    )
                    user_responce = UserAuthResponce(
                        id = user_sudo.id,
                        name = check_data(user_sudo.name),
                        email= check_data(user_sudo.email),
                        company_id = user_sudo.company_id.id,
                        company_name = check_data(user_sudo.company_id.name),
                        access_token = accessToken,
                        refresh_token = refreshToken,
                        is_complete = user_sudo.is_complete
                    )
                    return vars(user_responce)
                 else:  
                   raise ParamsErrorException("confirmation code is not equal")
                else:  
                   raise ParamsErrorException("the user is completed") 
            else: 
               raise ParamsErrorException("user_not_found")
        else: raise ParamsErrorException("the key confirmation code is not found in json bady")
 

    @staticmethod
    def changePassword():
        fetchRequestLanguage()
        args =  request.get_json_data()
        if 'new_password' in args:
            new_password = int(args.get('new_password'))
            user_sudo = request.env[ModelsName.usersRES].sudo().search(
                    [('partner_id', '=', request.jwt_partner_id)], limit=1)
            if user_sudo:
                    user_sudo.change_password(password=new_password)
                    #revoked_token 
                    token = request.env["ir.http"]._get_bearer_token()
                    user_confirmToken = request.env[ModelsName.matlobUsersTokens].sudo().search(
                    [('token', '=', token)], limit=1)
                    user_confirmToken.revoked_token()
                    return 'ok'                  
            else: 
               raise ParamsErrorException("user not found")
        else: raise ParamsErrorException("the key new password is not found in json bady")
 

