# coding: utf-8 -*-

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    advance_ids = fields.One2many('account.advanced.payment', 'move_id')
    advance_apply_ids = fields.One2many('account.advanced.payment', 'move_apply_id')
    advance_refund_ids = fields.One2many('account.advanced.payment', 'move_refund_id')