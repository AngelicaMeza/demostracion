# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _

class Picking(models.Model):
    _inherit = "stock.picking"

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if not res.move_lines:
            # Check if there are ops not linked to moves yet
            for pick in res:
                if pick.owner_id:
                    pick.move_lines.write({'restrict_partner_id': pick.owner_id.id})
                    pick.move_line_ids.write({'owner_id': pick.owner_id.id})
                for ops in pick.move_line_ids.filtered(lambda x: not x.move_id):
                    # Search move with this product
                    moves = pick.move_lines.filtered(lambda x: x.product_id == ops.product_id)
                    moves = sorted(moves, key=lambda m: m.quantity_done < m.product_qty, reverse=True)
                    if moves:
                        ops.move_id = moves[0].id
                    else:
                        new_move = self.env['stock.move'].create({
                                                        'name': _('New Move:') + ops.product_id.display_name,
                                                        'product_id': ops.product_id.id,
                                                        'product_uom_qty': ops.qty_done,
                                                        'product_uom': ops.product_uom_id.id,
                                                        'description_picking': ops.description_picking,
                                                        'location_id': pick.location_id.id,
                                                        'location_dest_id': pick.location_dest_id.id,
                                                        'picking_id': pick.id,
                                                        'picking_type_id': pick.picking_type_id.id,
                                                        'restrict_partner_id': pick.owner_id.id,
                                                        'company_id': pick.company_id.id,
                                                    })
                        ops.move_id = new_move.id
        if res.move_lines and res.picking_type_id.code == 'incoming':
            res.state = 'assigned'
        return res
