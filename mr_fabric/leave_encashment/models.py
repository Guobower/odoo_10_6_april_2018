# -*- coding: utf-8 -*-
import re
from openerp import models, fields, api
from openerp.exceptions import Warning, ValidationError, UserError

class LeaveForm(models.Model):
	_name = 'leave.encashment'
	_rec_name = 'date'

	date_from = fields.Date(string="Date From",required=True)
	date_to = fields.Date(string="Date To",required=True)
	date = fields.Char()
	laeve_id = fields.One2many('leave.encashment.tree','laeve_tree')

	@api.onchange('date_from','date_to')
	def get_rec(self):
		if self.date_from and self.date_to:
			self.date = self.date_from + "____" + self.date_to

class LeaveTree(models.Model):
	_name = 'leave.encashment.tree'

	card_no = fields.Many2one('emp.card.num',string="Card No",required=True)
	name = fields.Many2one('hr.employee',string="Name")
	designation = fields.Many2one('hr.job',string="Designation")
	date = fields.Date(string="Date")
	salary = fields.Float(string="Salary @ Month")
	bal_leaves = fields.Integer(string="Balance Leaves",default=14)
	net_amount = fields.Float(string="Net Amount")
	laeve_tree = fields.Many2one('leave.encashment')

	@api.onchange('card_no','name','bal_leaves')
	def get_rec(self):
		if self.bal_leaves == 14:
			if self.card_no and not self.name:
				rec = self.env['hr.employee'].search([('card_no.id','=',self.card_no.id)])
				self.name = rec.id
				self.designation = rec.job_id.id
				self.salary = rec.salary
			if self.name and not self.card_no:
				self.card_no = self.name.card_no.id
				self.designation = self.name.job_id.id
				self.salary = self.name.salary
			if self.salary > 0:
				self.net_amount = (self.salary/26) * self.bal_leaves
		if self.bal_leaves != 14 and self.salary > 0:
			self.net_amount = (self.salary/26) * self.bal_leaves


class SettleForm(models.Model):
	_name = 'settlement'

	card_no = fields.Many2one('emp.card.num',string="Card No.",required="True")
	name = fields.Many2one('hr.employee',string="Name")
	fname = fields.Char(string="Father Name")
	cnic = fields.Char(string="Cnic")
	designation = fields.Many2one('hr.job',string="Designation")
	shift = fields.Many2one('shifts.attendence',string="Shift")
	depart_id = fields.Many2one('hr.department',string="Department")
	date_app = fields.Date(string="Date Of Appointment")
	date_resign = fields.Date(string="Date Of S.o.S/Resign")
	settle_id = fields.One2many('settlement.tree','settle_tree')


	stages = fields.Selection([
	('draft','Draft'),
	('validated','Validated'),
	],default="draft")


	@api.multi
	def in_draft(self):
		self.stages = "draft"
						
	@api.multi
	def in_validate(self):
		self.stages = "validated"

	@api.multi 
	def unlink(self): 
		for x in self: 
			if x.stages == "validated": 
				raise ValidationError('Cannot Delete Record') 
		return super(InwardGatepassForm,self).unlink()


	@api.onchange('card_no')
	def get_record(self):
		if self.card_no:
			rec = self.env['hr.employee'].search([('card_no.id','=',self.card_no.id)])
			record = self.env['employee.resignation'].search([('employee_card.id','=',self.card_no.id)])
			self.name = rec.id
			self.designation = rec.job_id.id
			self.cnic = rec.cnic
			self.fname = rec.fname
			self.depart_id = rec.department_id.id
			self.shift = rec.schedule.id
			self.date_app = rec.doj
			self.date_resign = record.dor


class SettleTree(models.Model):
	_name = 'settlement.tree'
	_rec_name = 'types'


	types = fields.Many2one('settle.type',string="Type",required=True)
	name = fields.Char(string="Name")
	amount = fields.Float(string="Amount")
	settle_tree = fields.Many2one('settlement')

	@api.onchange('types')
	def get_type(self):
		if self.types:
			self.name = self.types.category




class SettleType(models.Model):
	_name = 'settle.type'
	_rec_name = 'name'

	name = fields.Char(string="Name")
	category = fields.Selection([('Allowances', 'SALARY & ALLOWWANCE '),('other','OTHRES'),('Deduction', 'Deduction')], string="Category")






