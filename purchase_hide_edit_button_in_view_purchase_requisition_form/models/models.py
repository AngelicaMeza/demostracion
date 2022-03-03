# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseRequisition(models.Model):

    _inherit = "purchase.requisition"

    x_css = fields.Html(string='CSS', sanitize=False, compute='_compute_css', store=False)

    @api.depends('state')
    def _compute_css(self):
        for application in self:
            if (application.state in ['open', 'done', 'cancel']) and not (self.env.user.has_group('purchase.group_purchase_manager')):
                application.x_css = '<style>.o_form_button_edit {display: none !important;}</style>'
            else:
                application.x_css = False

