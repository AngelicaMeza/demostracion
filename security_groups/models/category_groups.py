
from odoo import models, fields, api

class ProductCategopryGroup(models.Model):
	_inherit = 'product.category'
	product_category_groups = fields.Many2many(comodel_name='res.groups', string="Grupos que pueden ver productos de esta categoría")

class ProductTemplateCategoryGroup(models.Model):
	_inherit = 'product.template'
	
	def get_groups_category(self):
		for rec in self:
			id_groups = rec.categ_id.product_category_groups #Grupos que pueden ver la categoria
			uid = self._context.get('uid') #id del usuario actual
			user = self.env['res.users'].browse(uid) #objeto res.user del usuario actual
			if id_groups:
				for group in id_groups: #para cada grupo dentro de la categoria de producto
					if user in group.users:  #si el usuario actual esta dentro de algun grupo
						rec.can_see_product = True
						break
					else:
						rec.can_see_product = False
			else:
				rec.can_see_product = False
					
	can_see_product = fields.Boolean(compute= get_groups_category, default=False, string='Puede ver producto')

