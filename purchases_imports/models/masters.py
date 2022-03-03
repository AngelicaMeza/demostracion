from odoo import models, fields


class CustomsOffice(models.Model):
	_name = 'customs.office'
	_description = 'Customs'

	name = fields.Char(string = "Name")
	code = fields.Char(string = "Code")
	active = fields.Boolean('Active', default=True)

	_sql_constraints = [
		('unique_name', 'unique (code)', "There cannot be 2 customs with the same code."),
	]

	def name_get(self):
		result = []
		for item in self:
			item.search_name = item.code + '-' + item.name 
			result.append((item.id, item.search_name ))
		return result

class MerchandiseStatus(models.Model):
	_name = 'merchandise.status'
	_description = 'Merchandise Status'

	name = fields.Char(string = "Name")
	code = fields.Char(string = "Code")
	active = fields.Boolean('Active', default=True)
