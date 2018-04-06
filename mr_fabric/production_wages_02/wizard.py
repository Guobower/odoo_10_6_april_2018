from odoo import models, fields, api

class MrfabrictableForm(models.Model):
	_name = "mrfabric.table"

	employee = fields.Many2one('hr.employee',string="Employee")
	date = fields.Date(string="Confirmation Date")

	@api.onchange('employee')
	def onchange_date(self):
		self.date = self.employee.confirmation_date