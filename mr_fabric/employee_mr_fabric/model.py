# -*- coding: utf-8 -*- 
from odoo import models, fields, api
from datetime import date, datetime, timedelta

class EmployeeFormExtension(models.Model):
	_inherit = 'hr.employee'

	salaried_person = fields.Boolean(string="Salaried Person")
	rate_per_piece = fields.Boolean(string="Rate Per Piece")
	employee_type = fields.Selection([('temporary','Temporary'),('permanent','Permanent')],string='Employee Type',default='temporary')
	card_no = fields.Many2one('emp.card.num',string='Card No')
	schedule = fields.Many2one('shifts.attendence',string='Shift')
	dor = fields.Date(string='DOR')
	doj = fields.Date(string='Date of Joining')
	doi = fields.Date(string='Date of issue',default=fields.Date.today)
	confirmation_date = fields.Date(string='Confirmation Date')
	religion = fields.Selection([
		('muslim','Muslim'),
		('non_musliom','Non Muslim')
		],string='Religion',default='muslim')
	fname = fields.Char(string='Father Name')
	cnic = fields.Char(string='CNIC NO')
	social_security = fields.Boolean(string="Social Security")
	ss_no = fields.Char(string="SS No")
	eobi = fields.Boolean(string="EOBI")
	merchant = fields.Boolean(string="Merchant")
	eobi_no = fields.Char(string="EOBI No")
	name_card = fields.Char(string="Name")
	
	reff_name = fields.Char(string="Name")
	reff_city = fields.Char(string="City")
	reff_cnic = fields.Char(string="CNIC")
	reff_relation = fields.Char(string="Relation")
	qualification = fields.Char(string="Qualification")
	contact_address = fields.Char(string="Home Address")
	ntn = fields.Char(string="NTN")
	bank_account_id = fields.Char(string="Account Number")

	experience_tree = fields.One2many("hr.employee.experience","tree_link")
	leave_tree = fields.One2many("hr.employee.vocations","linked")
	bank = fields.Many2one("account.journal",string="Bank")
	incharge = fields.Many2one("hr.employee",string="Incharge")
	resigned = fields.Boolean(string="Resigned")

	salary = fields.Float(string="Salary")
	salary_structure = fields.Many2one('hr.payroll.structure',string="Salary Structure")

	@api.onchange('name','card_no')
	def onchange_namecard(self):
		addition = str(self.name) + ' - ' + str(self.card_no.name)
		self.name_card = addition

	@api.model
	def create(self, vals):
		new_record = super(EmployeeFormExtension, self).create(vals)

		newcontract = self.env['hr.contract'].create({
			'name': 'vals.name',
			'employee_id': 1,
			'department_id': self.department_id.id,
			'job_id': self.job_id.id,
			'wage': self.salary,
			'struct_id': self.salary_structure.id,
		})

		return new_record

	@api.model 
	def loan_ded(self, payslip):
		duration = 0.0 
		tsheet_obj = self.env['hr.overtime'] 
		timesheets = tsheet_obj.search([ ('date', '>=', payslip.date_from), ('date', '<=', payslip.date_to)]) 
		for x in timesheets: 
			for y in x.tree_link: 
				if y.employee.id==self.id: 
					duration = duration + y.overtime_amount 
		return duration

	@api.model 
	def loan_deduction_canteen(self, payslip):
		# result=employee.loan_deduction_canteen(payslip)
		duration = 0.0 
		tsheet_obj = self.env['ecube.detection'] 
		timesheets = tsheet_obj.search([('date', '>=', payslip.date_from),('date', '<=', payslip.date_to),('employee_id','=',self.id)])
		print timesheets
		for x in timesheets:
			print x.type_id.name
			if x.type_id.name == "Canteen":
				duration = duration + x.amount
		return duration

	@api.model 
	def loan_deduction_mobile(self, payslip):
		# result=employee.loan_deduction_mobile(payslip)
		duration = 0.0 
		tsheet_obj = self.env['ecube.detection'] 
		timesheets = tsheet_obj.search([('date', '>=', payslip.date_from),('date', '<=', payslip.date_to),('employee_id','=',self.id)])
		print timesheets
		for x in timesheets:
			print x.type_id.name
			if x.type_id.name == "Mobile":
				duration = duration + x.amount
		return duration

	def loan_deduction_advance(self, payslip):
		# result=employee.loan_deduction_advance(payslip)
		sumed = []
		total = 0.0

		timesheets = self.env['employee.advance'].search([('date', '>=', payslip.date_from),('date', '<=', payslip.date_to),('accessories_stages','=','approved')])
		
		for x in timesheets:
			for y in x.advance_tree:
				if y.employee_name.id == self.id:
					sumed.append(y.adv_request)

		for x in sumed:
			total = float(total) + float(x)
		
		return total

	def eobi_deduction(self, payslip):
		# result=employee.eobi_deduction(payslip)
		salary = 0
		total = 0

		employee = self.env['hr.employee'].search([('id','=',self.id)])
		salary = employee.salary

		if salary >= 15000:
			return salary/100
		else:
			return 0

	def tax_deduction(self, payslip):
		# result=employee.tax_deduction(payslip)
		salary = 0

		employee = self.env['hr.employee'].search([('id','=',self.id)])
		salary = employee.salary * 12

		if salary <= 400000:
			return 0

		elif salary > 400000 and salary <= 500000:
			return ((salary - 400000)*2)/100
		
		elif salary > 500000 and salary <= 750000:
			return (((salary - 500000)*5)/100) + 2000
		
		elif salary > 750000 and salary <= 1400000:
			return (((salary - 750000)*10)/100) + 14500
		
		elif salary > 1400000 and salary <= 1500000:
			return (((salary - 1400000)*12.5)/100) + 79500
		
		elif salary > 1500000 and salary <= 1800000:
			return (((salary - 1500000)*15)/100) + 92000
		
		elif salary > 1800000 and salary <= 2500000:
			return (((salary - 1800000)*17.5)/100) + 137000
		
		elif salary > 2500000 and salary <= 3000000:
			return (((salary - 2500000)*20)/100) + 259500
		
		elif salary > 3000000 and salary <= 3500000:
			return (((salary - 3000000)*22.5)/100) + 359500
		
		elif salary > 3500000 and salary <= 4000000:
			return (((salary - 3500000)*25)/100) + 472000
		
		elif salary > 4000000 and salary <= 7000000:
			return (((salary - 4000000)*27.5)/100) + 597000
		
		elif salary > 7000000:
			return (((salary - 7000000)*30)/100) + 1422000

class HrVocations(models.Model):
	_name = 'hr.employee.vocations'
	_rec_name = 'type'

	type = fields.Selection([
		('bychance','ByChance'),
		('annual','Annual'),
		('medical','Medical'),
	],default="bychance",string="Type")
	allowed = fields.Integer(string="Allowed")
	taken = fields.Integer(string="Taken")
	Left = fields.Integer(string="Left")

	linked = fields.Many2one('hr.employee')

	@api.onchange('allowed','taken')
	def onchange_allowed(self):
		if self.allowed and self.taken:
			self.Left = self.allowed - self.taken

class HrOvertime(models.Model):
	_name = 'hr.overtime'
	_rec_name = 'rec_name'

	date = fields.Date(string="Date", required= True)
	department = fields.Many2one('hr.department',string="Department")
	total_overtime_hours = fields.Float(string="Total Overtime Hours") 
	total_overtime_amount = fields.Float(string="Total Overtime Amount")
	tree_link = fields.One2many('hr.overtime.tree','tree_linked')
	rec_name = fields.Char(String="Rec name")

	@api.onchange('date','department')
	def onchange_depart(self):
		self.rec_name = str(self.department.name) + ',' + str(self.date)

	@api.onchange('tree_link')
	def onchange_tree(self):
		actual_overtime = 0
		total_overtime = 0
		for x in self.tree_link:
			actual_overtime = actual_overtime + x.actual_overtime_hours
			total_overtime = total_overtime + x.overtime_amount

		self.total_overtime_hours = actual_overtime
		self.total_overtime_amount = total_overtime

class HrOvertimeTreeView(models.Model):
	_name = 'hr.overtime.tree'

	employee = fields.Many2one('hr.employee',string="Employee", required= True)
	planed_overtime_hours = fields.Float(string="Planed Overtime Hours") 
	actual_overtime_hours = fields.Float(string="Actual Overtime Hours")
	overtime_rate = fields.Float(string="Overtime Rate")
	overtime_amount = fields.Float(string="Overtime Amount")
	remarks = fields.Char(string="Remarks")

	tree_linked = fields.Many2one('hr.overtime')

	@api.onchange('actual_overtime_hours','overtime_rate')
	def onchange_actual(self):

		self.overtime_amount = self.overtime_rate * self.actual_overtime_hours

class EmployeExperience(models.Model):
	_name = 'hr.employee.experience'

	comany_name = fields.Char(string="Company Name")
	city = fields.Char(string="City")
	designation = fields.Char(string="Designation")
	salary = fields.Char(string="Salary")
	job_period = fields.Char(string="Job Period")
	dor = fields.Char(string="DOR")
	resignation_reason = fields.Char(string="Resignation Reason")

	tree_link = fields.Many2one("hr.employee")

class PromotionTransfer(models.Model):
	_name = 'promotion.transfer'
	_rec_name = 'employee_name'

	date = fields.Date(string="Date", required=True)
	employee_name = fields.Char(string="Employee Name")
	employee_card = fields.Many2one('emp.card.num',string='Employee Card', required=True)
	current_designation = fields.Many2one('hr.job',string="Current Designation")
	current_department = fields.Many2one('hr.department',string="Current Department") 
	current_salary = fields.Char(string="Current Salary")
	doj = fields.Date(string="Date of Joining")
	proposed_designation = fields.Many2one('hr.job',string="Proposed Designation")
	proposed_department = fields.Many2one('hr.department',string="Proposed Department")
	proposed_salary = fields.Char(string="Proposed Salary")
	edp = fields.Date(string="Effected Date of Promotion")

	accessories_stages = fields.Selection([('draft','Draft'),('waiting_Approval','Waiting for Approval'),('approved','Approved')],string='Accessories Stages',default='draft')
	
	employee_card_replace = fields.Many2one('emp.card.num',string='Employee Card')
	employee_name_replace = fields.Char(string="Employee Name")
	department_replace = fields.Many2one('hr.department',string="Department")
	salary_replace = fields.Char(string="Salary")
	designation_replace = fields.Many2one('hr.job',string="Designation")
						
	@api.multi
	def in_draft(self):
		self.accessories_stages = "draft"
						
	@api.multi
	def in_waiting(self):
		self.accessories_stages = "waiting_Approval"
						
	@api.multi
	def in_approved(self):
		self.accessories_stages = "approved"
						
	@api.multi
	def in_validate(self):
		employee = self.env['hr.employee'].search([('card_no.id','=',self.employee_card.id)])
		employee.job_id = self.proposed_designation.id
		employee.department_id = self.proposed_department.id    

	@api.onchange('employee_card')
	def onchange_employee_card(self):
		employee = self.env['hr.employee'].search([('card_no.id','=',self.employee_card.id)])
		self.employee_name = employee.name
		self.current_designation = employee.job_id.id
		self.current_department = employee.department_id.id
		self.doj = employee.doj

		# contracts = self.env['hr.contract'].search([('employee_id.id','=',self.employee_name.id)])
		# self.current_salary = contracts.wage

	@api.onchange('employee_card_replace')
	def onchange_employee_card_replace(self):
		employee = self.env['hr.employee'].search([('card_no.id','=',self.employee_card_replace.id)])
		self.employee_name_replace = employee.name
		self.designation_replace = employee.job_id.id
		self.department_replace = employee.department_id.id

		# contracts = self.env['hr.contract'].search([('employee_id.id','=',self.employee_name_replace.id)])
		# self.current_salary = contracts.wage

class EmployeeResignation(models.Model):
	_name = 'employee.resignation'
	_rec_name = 'employee_name'

	date = fields.Date(string="Date", required=True)
	employee_name = fields.Char(string="Employee Name")
	employee_card = fields.Many2one('emp.card.num',string='Employee Card', required=True)
	designation = fields.Many2one('hr.job',string="Designation")
	department = fields.Many2one('hr.department',string="Department") 
	fname = fields.Char(string="Father Name")
	dor = fields.Date(string="Date of Resignation")

	accessories_stages = fields.Selection([('draft','Draft'),('clearance','Clearance'),('waiting_approval','Waiting for Approval'),('approved','Approved'),('cancel','Cancel')],string='Accessories Stages',default='draft')
 
	@api.multi
	def in_draft(self):
		self.accessories_stages = "draft"
						
	@api.multi
	def in_clearance(self):
		employee = self.env['hr.employee'].search([('card_no.id','=',self.employee_card.id)])
		for x in employee:
			x.resigned = True
		self.accessories_stages = "clearance"
						
	@api.multi
	def in_waiting(self):
		self.accessories_stages = "waiting_approval"
						
	@api.multi
	def in_approved(self):
		self.accessories_stages = "approved"
		employee = self.env['hr.employee'].search([('card_no.id','=',self.employee_card.id)])
		for x in employee:
			x.active = False
						
	@api.multi
	def in_cancel(self):  
		self.accessories_stages = "cancel"

	@api.onchange('employee_card')
	def onchange_employee_card(self):
		employee = self.env['hr.employee'].search([('card_no.id','=',self.employee_card.id)])
		self.employee_name = employee.name
		self.designation = employee.job_id.id
		self.department = employee.department_id.id

class EmployeeCardNum(models.Model):
	_name = 'emp.card.num'
	_rec_name = 'name'

	name = fields.Char(string="Name")

class EmployeeAdvance(models.Model):
	_name = 'employee.advance'
	_rec_name = 'department'

	date = fields.Date(string="Date", required=True)
	department = fields.Many2one('hr.department',string="Department")

	advance_tree = fields.One2many("employee.advance.tree","tree_link")

	accessories_stages = fields.Selection([('draft','Draft'),('waiting_approval','Waiting for Approval'),('approved','Approved'),('cancel','Cancel')],string='Accessories Stages',default='draft')
 
	@api.multi
	def in_draft(self):
		self.accessories_stages = "draft"
						
	@api.multi
	def in_waiting(self):
		self.accessories_stages = "waiting_approval"
						
	@api.multi
	def in_approved(self):
		self.accessories_stages = "approved"
						
	@api.multi
	def in_cancel(self):  
		self.accessories_stages = "cancel"

class EmployeeAdvanceTreeView(models.Model):
	_name = 'employee.advance.tree'
	_rec_name = 'employee_name'

	employee_name = fields.Many2one('hr.employee',string="Employee Name")
	employee_card = fields.Many2one('emp.card.num',string='Employee Card', required=True)
	designation = fields.Many2one('hr.job',string="Designation")
	salary = fields.Char(string="Salary")
	adv_request = fields.Char(string="Adv. Request")
	remarks = fields.Char(string="Remarks")
	approved = fields.Boolean(string="Approved")

	tree_link = fields.Many2one("employee.advance")

	@api.onchange('employee_card')
	def onchange_employee_card(self):
		employee = self.env['hr.employee'].search([('card_no.id','=',self.employee_card.id)])
		self.employee_name = employee.id
		self.designation = employee.job_id.id
		self.salary = employee.salary

class EmployeeIncrement(models.Model):
	_name = 'employee.increment'
	_rec_name = 'employee_name'

	employee_name = fields.Char(string="Employee Name")
	fname = fields.Char(string="Father Name")
	employee_card = fields.Many2one('emp.card.num',string='Employee Card', required=True)
	date = fields.Date(string="Date")
	doj = fields.Date(string="Date Of Joining")
	doc = fields.Date(string="Date Of Confirmation")

	increment = fields.Integer(string="Increment")

	@api.onchange('employee_card')
	def onchange_employee_card(self):
		employee = self.env['hr.employee'].search([('card_no.id','=',self.employee_card.id)])
		self.employee_name = employee.name
		self.fname = employee.fname
		self.doj = employee.doj
		self.doc = employee.confirmation_date

class OrientationTraining(models.Model):
	_name = 'orientation.training'
	_rec_name = 'employee_name'

	employee_name = fields.Char(string="Employee Name")
	employee_card = fields.Many2one('emp.card.num',string='Employee Card', required=True)
	department = fields.Many2one('hr.department',string="Department")
	designation = fields.Many2one('hr.job',string="Designation")

	@api.onchange('employee_card')
	def onchange_employee_card(self):
		employee = self.env['hr.employee'].search([('card_no.id','=',self.employee_card.id)])
		self.employee_name = employee.name
		self.department = employee.department_id.id
		self.designation = employee.job_id.id

class SalarayRulesExtension(models.Model):
	_inherit = "hr.salary.rule"

	urdu_name = fields.Char(string="Urdu Name")