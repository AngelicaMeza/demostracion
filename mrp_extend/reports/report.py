from odoo import models

class ReportBomStructure(models.AbstractModel):
    _inherit = 'report.mrp.report_bom_structure'

    def _get_bom(self, bom_id=False, product_id=False, line_qty=False, line_id=False, level=False):
        res = super(ReportBomStructure, self)._get_bom(bom_id, product_id, line_qty, line_id, level)
        
        res['route'] = res['bom'] and res['bom'].routing_id or ''
        res['route_name'] = res['bom'].routing_id.display_name or ''
        # res['ecos'] = self.env['mrp.eco'].search_count([('product_tmpl_id', '=', product_tmpl_id), ('state', '!=', 'done')]) or ''
        return res

    def _add_production_routes(self, components):
        for line in components:
            child_bom = line.get('child_bom')
            route = line.get('parent_id')
            route_id = ''
            if child_bom:
                child_bom = self.env['mrp.bom'].browse(child_bom)
                route_id = self.env['mrp.bom'].search([('id', '=', child_bom.id)]).routing_id or ''
            # elif route:
            #     # child_bom = self.env['mrp.bom'].browse(child_bom)
            #     route_id = self.env['mrp.bom'].search([('id', '=', route)]).routing_id.display_name or ''


            line['route'] = route_id or ''
            line['route_name'] = route_id.display_name if route_id else ''



    def _get_bom_lines(self, bom, bom_quantity, product, line_id, level):
        components, total = super(ReportBomStructure, self)._get_bom_lines(bom, bom_quantity, product, line_id, level)
        self._add_production_routes(components)
        return components, total

    def _get_pdf_line(self, bom_id, product_id=False, qty=1, child_bom_ids=[], unfolded=False):
        data = super(ReportBomStructure, self)._get_pdf_line(bom_id, product_id, qty, child_bom_ids, unfolded)
        self._add_production_routes(data['lines'])
        return data