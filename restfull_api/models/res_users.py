# -*- coding: utf-8 -*-
import random


from odoo import _, fields, models
from ..utils.models_name import ModelsName

class ResUser(models.Model):
    _inherit = ModelsName.usersRES
    
    confirmation_code = fields.Integer(
        string="Confirmation Code", readonly=True)
    is_complete = fields.Boolean(readonly=True, default=False) 

    def random_confirmation_code(self):
        for rec in self:
            rec.confirmation_code = random.randint(100000, 999999)

    def change_password(self,password):
        for rec in self:
            rec.password = password
    