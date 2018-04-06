from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    machine_int = fields.Integer(string='Machine ID')


HrEmployee()


class EmployeeContract(models.Model):
    _inherit = 'hr.contract'
    delay_struct_id = fields.Many2one(comodel_name='delay.structure', string='Delay Structure')


EmployeeContract()
