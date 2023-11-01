from  ..utils.models_name import ModelsName
from odoo import fields, models

class UsersToken(models.Model):
    _name = ModelsName.authUsersTokens  
    # Replace with your module and model name

    # Add fields
    token = fields.Char(unique=True)
    refresh_token = fields.Char(unique=True)
    type = fields.Char('type')
    revoked = fields.Boolean(readonly=True, default=False)
    user_id = fields.Many2one('res.users', int='User')


    def revoked_token(self):
        for rec in self:
            rec.revoked = True
            
    def update_token(self,token):
        for rec in self:
            rec.token = token

    @staticmethod
    def toMap(token,refresh_token,user_id,type,revoked=False):
       return {'token':token,"refresh_token":refresh_token,'user_id':user_id,'type':type,'revoked':revoked}   