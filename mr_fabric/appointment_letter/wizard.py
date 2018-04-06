from odoo import models, fields, api

class AppointmentLetterForm(models.Model):
	_name = "appointment.letter"

	card_no = fields.Many2one('emp.card.num',string="Card No.", required="1")
	employee = fields.Many2one('hr.employee',string="Employee")
	date = fields.Date(string="Confirmation Date")

	@api.onchange('card_no')
	def onchange_employee_card(self):
		employee = self.env['hr.employee'].search([('card_no.id','=',self.card_no.id)])
		self.employee = employee.id
		self.date = employee.confirmation_date