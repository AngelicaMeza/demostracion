# -*- coding: utf-8 -*-

from odoo import models, fields, api


class users_warehouse(models.Model):
    _inherit="res.users"

    user_warehouse_id = fields.Many2many("stock.warehouse")

class aprove_flow(models.Model):
    _inherit="stock.picking"

    @api.depends('picking_type_id')
    def compute_locations(self):
        if self.picking_type_id:
            for rec in self:
                for child in rec.env.user.user_warehouse_id:
                    self.warehouse_locations += child.lot_stock_id.compute_childs()
        else:
            self.warehouse_locations = False

    warehouse_locations = fields.One2many('stock.location','location_id', compute=compute_locations, readonly='True')

class requisition(models.Model):
    _inherit = "stock.picking.type"

    def am_i_admin(self):
        self.im_admin = self.env.user.has_group('stock.group_stock_manager')

    im_admin = fields.Boolean(compute=am_i_admin )

class stocklocation(models.Model):
    _inherit="stock.location"

    def compute_childs(self):
        childs = self.browse(self.id)
        for child in self.child_ids:
            if child.child_ids:
                childs += child.compute_childs()
            else:
                childs += self.browse(child.id)
        return childs

    def compute_field(self):
        for warehouse in self.env.user.user_warehouse_id:
            self.childs_ids_all += warehouse.lot_stock_id.compute_childs()

    childs_ids_all = fields.One2many('stock.location', 'location_id', compute=compute_field)
