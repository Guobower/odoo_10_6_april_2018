# -*- coding: utf-8 -*- 
from odoo import models, fields, api
from openerp.exceptions import Warning, ValidationError, UserError
import datetime
import datetime as dt

class HrContracts(models.Model):
    _inherit = 'hr.contract'

    mobile = fields.Char(string="Mobile")
    fuel = fields.Char(string="Fuel")
    tax = fields.Char(string="Tax")
    eobi = fields.Char(string="EOBI")
    advance = fields.Char(string="Advance")
    canteen = fields.Char(string="Canteen")

    wage = fields.Float(string="Salary")

    advantages = fields.Text(string="Advantages")
    
    days = fields.Char(string="No of Working Days")
    hours = fields.Char(string="Overtime Hours")
    schedule = fields.Many2one('shifts.attendence',string='Shift')

    @api.onchange('employee_id')
    def get_structures(self):
    	self.wage = self.employee_id.salary
    	self.struct_id = self.employee_id.salary_structure.id
    	self.schedule = self.employee_id.schedule.id

class EcubeAllowanceClass(models.Model):
	_name = 'ecube.allowance'
	_rec_name = 'employee_id'

	description = fields.Text(string="Description")
	amount = fields.Float(string="Amount", required=True)

	employee_id = fields.Many2one('hr.employee',string="Employee", required=True)
	type_id = fields.Many2one('ecube.allowance.type',string="Type", required=True)

	date = fields.Date(string="Date", required=True)

class EcubeDetectionClass(models.Model):
	_name = 'ecube.detection'
	_rec_name = 'employee_id'

	description = fields.Text(string="Description")
	amount = fields.Float(string="Amount", required=True)

	employee_id = fields.Many2one('hr.employee',string="Employee", required=True)
	type_id = fields.Many2one('ecube.allowance.type',string="Type", required=True)

	date = fields.Date(string="Date", required=True)

class EcubePayrollTypeClass(models.Model):
    _name = 'ecube.allowance.type'
    _rec_name = 'name'

    name = fields.Char(string="Name")

class WagePerPiece(models.Model):
    _name = 'wage.per.piece'
    _rec_name = 'production'

    form = fields.Date(string="From")
    to = fields.Date(string="To")
    
    style_name = fields.Char(string="Style Name")
    decrip = fields.Text(string="Description")

    production = fields.Many2one('purchase.production.unit',string="Production Unit",required=True)
    won = fields.Many2one('mrp.production',string="WO No",required=True)
    style = fields.Many2one('style.number',string="Style No")
    tree_link = fields.One2many('wage.piece.tree','link')

    @api.onchange('won')
    def get_structures(self):

        self.style = self.won.style_no.id

class WagePerPieceTree(models.Model):
    _name = 'wage.piece.tree'
    _rec_name = 'operation'

    qty = fields.Float(string="Qty Pcs")
    rate = fields.Float(string="Rate @ DZN")
    amount = fields.Float(string="Amount")
    
    operation = fields.Char(string="Operation")

    machine = fields.Many2one('machine.wages',string="Machine")
    employee_id = fields.Many2one('hr.employee',string="Employee")
    card_no = fields.Many2one('emp.card.num',string="Card No",required=True)
    link = fields.Many2one('wage.per.piece')

    @api.onchange('card_no')
    def picking_type(self):
        if self.card_no:
            employee = self.env['hr.employee'].search([('card_no.id','=',self.card_no.id)])
            for x in employee:
                self.employee_id = x.id

    @api.onchange('qty','rate')
    def quantity(self):
        if self.qty or self.rate:
            self.amount = (self.qty * (self.rate/12))

class EcubeMachineClass(models.Model):
    _name = 'machine.wages'
    _rec_name = 'name'

    name = fields.Char(string="Name")

class HrContracts(models.Model):
    _inherit = 'res.users'

    department = fields.Many2one('hr.department',string="Department")