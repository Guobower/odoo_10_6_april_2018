from openerp import models, fields, api
from openerp.exceptions import Warning
from odoo.exceptions import UserError
from openerp.exceptions import UserError


class EcubeRawAttendance(models.Model):
	_name = 'ecube.raw.attendance'
	_description = 'EcubeRawAttendance'
	name = fields.Char('Employee Name')
	machine_id = fields.Char('Employee Machine id')
	machine_date = fields.Date('Date')
	machine_time = fields.Date('Time')
	employee_id = fields.Many2one('hr.employee',string="Employee")
