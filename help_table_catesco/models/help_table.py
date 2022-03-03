# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.translate import _


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    report = fields.Binary('Informe del Distribuidor')

    client_name = fields.Many2one('res.partner', string='Nombre del Cliente')
    proceed_claim = fields.Boolean(string='Procede el reclamo')
    amount_by = fields.Integer(string='Cantidad')
    warranty_id = fields.Many2one(
        'helpdesk.warrantycodes', string='Warranty Codes')
    defect_id = fields.Many2one(
        'helpdesk.defectcode', string='Nombre del Cliente')
    second_product = fields.Many2one('product.product', string='Medida')
    tier_brand_id = fields.Many2one('helpdesk.tierbrand', string='Marca')
    week_serial = fields.Char(string='Serial de Semana')
    wear_percentagenta = fields.Float('Desgaste')
    percent_sale_price = fields.Float('reconocido del precio de venta')

    car_brand_id = fields.Many2one('helpdesk.carbrand', string='Marca')
    year_by = fields.Integer(string='year')
    mileage = fields.Float('Kilometraje')
    car_model_id = fields.Many2one('helpdesk.carmodel', string='Modelo')
    placa = fields.Char(string='Placas')
    long_distance = fields.Boolean(string='Larga distancia')
    regional = fields.Boolean(string='Regional')
    city = fields.Boolean(string='Ciudad')
    mix_service = fields.Boolean(string='Servicio mixto')
    out_road = fields.Boolean(string='Fuera de carretera')


class WarrantyCodes(models.Model):
    _name = 'helpdesk.warrantycodes'

    _description = 'Warranty Codes'

    name = fields.Char(
        'Código de Garantía', size=64,
        # required=True,
        # readonly=False,
        # default=None,
        help="Códigos de Garantía")
    
    descripcion = fields.Char(
        'Descripcion', size=64,
        # required=True,
        # readonly=False,
        # default=None,
        help="descripcion")

    def name_get(self):
        result = []
        for rec in self:
            name = rec.name +' - '+ rec.descripcion
            result.append((rec.id,name))

        return result
    


class DefectCode(models.Model):
    _name = 'helpdesk.defectcode'
    _description = 'defect Codes'

    name = fields.Char(
        'Código de Defectos', size=64,
        # required=True,
        # readonly=False,
        # default=None,
        help="Código de Defectos")

    descripcion = fields.Char(
        'Descripcion', size=64,
        # required=True,
        # readonly=False,
        # default=None,
        help="descripcion")

    def name_get(self):
        result = []
        for rec in self:
            name = rec.name +' - '+ rec.descripcion
            result.append((rec.id,name))

        return result


class BrandCode(models.Model):
    _name = 'helpdesk.tierbrand'
    _description = 'Tier Brand'

    name = fields.Char(
        'Marca', size=64,
        # required=True,
        # readonly=False,
        # default=None,
        help="Marca")


class CarBrand(models.Model):
    _name = 'helpdesk.carbrand'
    _description = 'car brand'

    name = fields.Char(
        'Marca', size=64,
        # required=True,
        # readonly=False,
        # default=None,
        help="Marca")

class CarModel(models.Model):
    _name = 'helpdesk.carmodel'
    _description = 'Car Model'

    name = fields.Char(
        'Marca', size=64,
        # required=True,
        # readonly=False,
        # default=None,
        help="Modelo")

    car_brand_id = fields.Many2one('helpdesk.carbrand', string='Marca')
