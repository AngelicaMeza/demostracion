# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.translate import _
class AccountMoveReversal(models.TransientModel):

    _inherit = 'account.move.reversal'
    # refund_method = fields.Selection(selection=[
    #         ('refund', 'Partial Refund')], string='Credit dddddddddMethod', required=True,
    #     help='Choose how you want to credit this invoice. You cannot "modify" nor "cancel" if the invoice is already reconciled.')




    @api.model
    def default_get(self, fields):
        res = super(AccountMoveReversal, self).default_get(fields)
        # move_ids = self.env['account.move'].browse(self.env.context['active_ids']) if self.env.context.get('active_model') == 'account.move' else self.env['account.move']
        res['refund_method'] = 'refund'
    
        return res
