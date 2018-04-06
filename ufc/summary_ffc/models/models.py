from odoo import models, fields, api

class summary_ffc(models.Model):
	_name = 'summary.ffc'
	_rec_name = 'name'

	name          		= fields.Char(compute = '_computed_field')
	Customer 			= fields.Many2one('res.partner',string="Customer")
	Branch 				= fields.Many2one('branch',string="Branch")
	Region 				= fields.Char()
	amt_total 			= fields.Float(string="Amount Total")
	invoice_date 		= fields.Date(string="Invoice Date")
	date_from 			= fields.Date()
	date_to 			= fields.Date()
	bill_no 			= fields.Char(string="Bill No")
	pun_fuel_deduct 	= fields.Float(string="Punjab Fuel Deduction")
	sin_fuel_deduct 	= fields.Float(string="Sindh Fuel Deduction")
	m_tons_punjab 		= fields.Char(string="M Tons Punjab")
	m_tons_sindh 		= fields.Char(string="M Tons Sindh")
	val_excl_punjab_st  = fields.Float(string="Value Excel Punjab S.T")
	val_excl_sindh_st   = fields.Float(string="Value Excel Sindh S.T")
	pun_invoice 		= fields.Many2one('account.invoice',string="Punjab Invoice")
	sin_invoice 		= fields.Many2one('account.invoice',string="Sindh Invoice")
	invoice_link 		= fields.Many2one('account.invoice',string="Invoice Link")
	sum_ids 			= fields.One2many('summary.tree','sum_id')
	sum_ids2 			= fields.One2many('ufc.auto','ufc_summary')
	value_ids 			= fields.One2many('ufc.auto','ufc_dharki')
	stages    			= fields.Selection([
        				('draft', 'Draft'),
        				('validate', 'Validate'),
        				],default='draft')

# ==============================giving rec name by computed function =======================
# ==============================giving rec name by computed function =======================

	@api.depends('Customer')
	def _computed_field(self):
		if self.Customer:
			self.name = "Summary of "+str(self.Customer.name)


	@api.multi
	def draft(self):
		self.stages = "draft"

# ===========================updating invoice already created on generate button==============
# ===========================updating invoice already created on generate button==============

	@api.multi
	def validate(self):
		self.stages = "validate"

		if self.Customer:
			records = self.env['account.invoice'].search([('summary_id','=',self.id)])
			if self.Customer.name== "FFC Goth Machi" or self.Customer.name== "FFC Mir Pur Mathelo":

				for data in records:
					if data.province == "Punjab":
						data.partner_id = self.Customer.id
						data.date_invoice = self.invoice_date
						data.bill_no = self.bill_no
						data.province = "Punjab"
						data.branch = self.Branch.id
						data.m_tons = self.m_tons_punjab
						data.invoice_line_ids.name = "Value Excel Punjab S.T"
						data.invoice_line_ids.price_unit = self.val_excl_punjab_st
					if data.province == "Sindh":
						data.partner_id = self.Customer.id
						data.date_invoice = self.invoice_date
						data.bill_no = self.bill_no
						data.province = "Sindh"
						data.branch = self.Branch.id
						data.m_tons = self.m_tons_sindh
						data.invoice_line_ids.name = "Value Excel Punjab S.T"
						data.invoice_line_ids.price_unit = self.val_excl_sindh_st
			
			else:

				for data in records:
				
					data.partner_id = self.Customer.id
					data.date_invoice = self.invoice_date
					data.bill_no = self.bill_no
					data.branch = self.Branch.id
					data.invoice_line_ids.name = "Company Price"
					data.invoice_line_ids.price_unit = self.amt_total
					

# ===================creating Customer invoice on generate button from bill summary===========			
# ===================creating Customer invoice on generate button from bill summary===========			


	@api.multi
	def generate(self):
		
		if self.Customer.name== "FFC Goth Machi" or self.Customer.name== "FFC Mir Pur Mathelo":

			records = self.env['account.invoice'].create({
				'partner_id':self.Customer.id,
				'date_invoice':self.invoice_date,
				'bill_no':self.bill_no,
				'province':"Punjab",
				'branch':self.Branch.id,
				'm_tons': self.m_tons_punjab,
				'summary_id': self.id

				})

			self.pun_invoice = records.id

			records.invoice_line_ids.create({
				'name':"Value Excel Punjab S.T",
				'price_unit':self.val_excl_punjab_st,
				'account_id':17,
				'quantity':1,
				'invoice_id' : records.id

				})

			records_sin = self.env['account.invoice'].create({
				'partner_id':self.Customer.id,
				'date_invoice':self.invoice_date,
				'bill_no':self.bill_no,
				'province':"Sindh",
				'branch':self.Branch.id,
				'm_tons': self.m_tons_sindh,
				'summary_id': self.id
				})

			self.sin_invoice = records_sin.id

			records_sin.invoice_line_ids.create({
				'name':"Value Excel Sindh S.T",
				'price_unit':self.val_excl_sindh_st,
				'account_id':17,
				'quantity':1,
				'invoice_id' : records_sin.id

				})

		else:

			data = self.env['account.invoice'].create({
				'partner_id':self.Customer.id,
				'date_invoice':self.invoice_date,
				'bill_no':self.bill_no,
				'branch':self.Branch.id,
				'summary_id': self.id

				})

			self.invoice_link = data.id

			data.invoice_line_ids.create({
				'name':"Company Price",
				'price_unit':self.amt_total,
				'account_id':17,
				'quantity':1,
				'invoice_id' : data.id

				})

# =========================creating models and tree view required for bill summary===========
# =========================creating models and tree view required for bill summary===========

class summary_tree(models.Model):
	_name = 'summary.tree'

	Region 		= fields.Char()
	region_name = fields.Char(string="Region Name")
	Sheet 		= fields.Char()
	M_tons 		= fields.Char(string="M Tons")
	Amount 		= fields.Char()
	Remarks 	= fields.Char()
	sum_id 		= fields.Many2one('summary.ffc')


class ufc_auto_tree(models.Model):
	_inherit = 'ufc.auto'

	ufc_summary = fields.Many2one('summary.ffc')
	ufc_dharki = fields.Many2one('summary.ffc')
