
from odoo import models, fields, api
from odoo.osv.expression import AND


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.model
    def _check_permit_moves(self):
        select = '''
            select distinct sm.id
            from stock_move sm
            inner join product_product pp on pp.id = sm.product_id
            inner join product_template pt on pt.id = pp.product_tmpl_id
            inner join product_category pc on pc.id = pt.categ_id
            left join product_category_res_groups_rel pcg on pcg.product_category_id = pc.id
        '''
        where = '''  
            where pcg.res_groups_id is null or pcg.res_groups_id in %s
        '''
        order_by = 'order by sm.id'

        query = "{}\n{}\n{}".format(select, where, order_by)
        self._cr.execute(query, (tuple(self.env.user.groups_id.ids),))
        res = self._cr.fetchall()
        move_ids = [res_id[0] for res_id in res]
        return self.browse(move_ids)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def _check_picking(self):
        query = """ 
            select sp.id
            from stock_picking sp
            inner join stock_move sm on sm.picking_id = sp.id
            inner join product_product pp on pp.id = sm.product_id
            inner join product_template pt on pt.id = pp.product_tmpl_id
            inner join product_category pc on pc.id = pt.categ_id
            left join product_category_res_groups_rel pcg on pcg.product_category_id = pc.id
            group by sp.id
            having 
            count(sm.id) =  sum(case when pcg.res_groups_id is null or pcg.res_groups_id in %s then
            1 else 0 end)
            order by sp.id
        """
        self._cr.execute(query, (tuple(self.env.user.groups_id.ids),))
        res = self._cr.fetchall()
        picking_ids = [res_id[0] for res_id in res]
        return self.browse(picking_ids)

    @api.model
    @api.returns('self',
        upgrade=lambda self, value, args, offset=0, limit=None, order=None, count=False: value if count else self.browse(value),
        downgrade=lambda self, value, args, offset=0, limit=None, order=None, count=False: value if count else value.ids)
    def search(self, args, offset=0, limit=None, order=None, count=False):
        pickings_permits = self._check_picking()
        args = AND([args, [('id', 'in', pickings_permits.ids)]])
        return super().search(args, offset, limit, order, count)
