# -- coding: utf-8 -
from odoo import _, api, fields, models, tools
import logging

logger = logging.getLogger("name_")


class AuthJwtValidator(models.Model):
    _inherit = 'auth.jwt.validator'

    partner_id_strategy = fields.Selection(selection_add=[('id', 'From ID Claim')])

    def _get_partner_id(self, payload):
        if self.partner_id_strategy == 'id':
            partner_id = payload.get('id')
            if not partner_id:
                logger.debug('JWT payload does not have an ID claim')
                return
            partner = self.env['res.partner'].sudo().search([('id', '=', partner_id)])
            if len(partner) != 1:
                logger.debug('%d partners found for ID %s', len(partner), partner_id)
                return
            return partner.id
        else:
            return super(AuthJwtValidator, self)._get_partner_id(payload=payload)