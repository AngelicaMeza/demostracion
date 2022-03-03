# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta

import logging
_logger = logging.getLogger(__name__)

class StockMove(models.Model):
    _inherit = 'stock.move'

    kardex_price_unit = fields.Float(string='Kardex Price Unit', default=0) # digits=(total, decimal)
    type_operation_sunat_id = fields.Many2one('type.operation.kardex','Tipo de Transacción')
    valoracion = fields.One2many(comodel_name='stock.valuation.layer', inverse_name='stock_move_id', string='Valoracion')
    
    def set_kardex_price_unit(self):
        total = 0 
        for item in self.valoracion : 
            total += item.value
        self.kardex_price_unit = total / self.product_qty 
        self.kardex_price_unit =  self.kardex_price_unit - self.price_unit 
        
  
class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    kardex_id = fields.One2many(comodel_name='product.product.kardex.line', inverse_name='template', string='Kardex')

class ProductProduct(models.Model):
    _inherit = 'product.product'

    kardex_id = fields.One2many(comodel_name='product.product.kardex.line', inverse_name='name', string='Kardex')

    def ver_kardex(self):
        self.generate_kardex_gb()
        action = self.env.ref('jp_kardex_valorizado.kardex_line_action').read()[0]

        pickings = self.env['product.product.kardex.line'].search([])
        if len(pickings) > 1:
            action['domain'] = [('id', 'in', pickings.ids)]
        return action

    def generate_kardex_gb(self):
        movimientos = self.env['stock.valuation.layer'].search([
            ('product_id','=',self.id),
         #   ('account_move_id','!=', False),
        ])
        temp =  self.env['product.product.kardex.line'].search([])
        for t in temp:
            t.unlink()
        saldo = 0
        saldo_total = 0
        promedio = 0

        for line in movimientos :
            ajuste = self.env['stock.inventory'].search([('move_ids','=',line.stock_move_id.id)])
            saldo +=  line.quantity
            saldo_total +=  line.value 
            promedio = saldo_total / saldo  if saldo > 0 else 0
            #
            if line.stock_move_id.type_operation_sunat_id.id:
                type_operation_sunat_id = line.stock_move_id.type_operation_sunat_id
            else : 
                type_operation_sunat_id = line.stock_move_id.picking_type_id.type_operation_sunat_id
            if ajuste:
                inventory_flag = 10
            else:
                inventory_flag = 1
            if line.quantity >= 0:
                self.env['product.product.kardex.line'].create({
                'name': self.id,
                'stock_move_id': inventory_flag,
                'fecha': line.date,
                'type_operation_sunat_id' : type_operation_sunat_id.id,
                'cantidad_entradas':line.quantity,
                'costo_entradas':line.unit_cost,
                'total_bolivares_entradas': line.value,
                'total':saldo,
                'promedio':promedio,
                'total_bolivares':saldo_total
                })
            else :
                self.env['product.product.kardex.line'].create({
                'name': self.id,
                'stock_move_id': inventory_flag,
                'fecha': line.date,
                'type_operation_sunat_id' : type_operation_sunat_id.id,
                'cantidad_salidas':line.quantity * -1 ,
                'costo_salidas': line.unit_cost , 
                'total_bolivares_salida': line.value * -1,
                'total':saldo,
                'promedio':  promedio,
                'total_bolivares':saldo_total
                })
       
   

class ProductKardexLine(models.TransientModel):
    _name = "product.product.kardex.line"

    template  = fields.Many2one(comodel_name='product.template', string='template')
    stock_move_id  = fields.Char(string='Movimiento')

    name  = fields.Many2one(comodel_name='product.product', string='Producto')
    type_operation_sunat_id = fields.Many2one('type.operation.kardex','Tipo de Transacción')

    fecha = fields.Date(string='Fecha')
    
    cantidad_inicial = fields.Float(string='Cantidad Incial')
    costo_intradas    = fields.Float(string='Costo de Inicial')
    total_bolivares_inicial   = fields.Float(string='Total Bolivares Inicial')

    category_id = fields.Many2one(comodel_name='product.category', string='Categoria')

    cantidad_entradas = fields.Float(string='Cantidad Entradas')
    costo_entradas    = fields.Float(string='Costo de Entradas')
    total_bolivares_entradas   = fields.Float(string='Total Bolivares ')

    cantidad_salidas  = fields.Float(string='Cantidad Salidas')
    costo_salidas     = fields.Float(string='Costo de Salidas')
    total_bolivares_salida     = fields.Float(string='Total Bolivares')

    total  = fields.Float(string='Total')
    promedio     = fields.Float(string='Promedio')
    total_bolivares     = fields.Float(string='Total Bolivares')
    
class StockScrap(models.Model):
    _inherit = 'stock.scrap'
  
    def action_validate(self):
        t = super(StockScrap, self).action_validate() 
        tipo = self.env['type.operation.kardex'].search([('id','=','14')])
        self.move_id.type_operation_sunat_id = tipo[0].id
        return t