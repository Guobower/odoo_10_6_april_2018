from odoo import models, fields, api

class summary_orient(models.Model):
	_name = 'orient.summ'
	_rec_name = 'name'

	name         = fields.Char(compute = '_computed_field')
	customer     = fields.Many2one('res.partner',string="Customer")
	branch       = fields.Many2one('branch',string="Branch")
	invoice_date = fields.Date(string="Invoice Date")
	loading_date = fields.Date(string="Loading Date")
	item         = fields.Char(string="Item")
	bill_no      = fields.Char(string="Bill No")
	weight       = fields.Float(string="Weight")
	number       = fields.Char(string="L/C Number")
	date_from    = fields.Date()
	date_to      = fields.Date()
	amt_total    = fields.Float(string="Amount Total")
	bl_number    = fields.Char(string="B/L Number")
	orient_link  = fields.Many2one('account.invoice',string="Invoice Link")
	sum_ids2     = fields.One2many('ufc.auto','orient_summary')
	stages       = fields.Selection([
        		('draft', 'Draft'),
        		('validate', 'Validate'),
        		],default='draft')

# ==========================giving rec name by computed function ============================
# ==========================giving rec name by computed function ============================

	@api.depends('customer')
	def _computed_field(self):
		if self.customer:
			self.name = "Summary of "+str(self.customer.name)


	@api.multi
	def draft(self):
		self.stages = "draft"

# ========================validating invoice already created on generate button===============
# ========================validating invoice already created on generate button===============

	@api.multi
	def validate(self):
		self.stages = "validate"

		if self.customer:
			records = self.env['account.invoice'].search([('summary_id','=',self.id)])

			for data in records:
				
				data.partner_id = self.customer.id
				data.date_invoice = self.invoice_date
				data.bill_num = self.bl_number
				data.branch = self.branch.id
				data.invoice_line_ids.name = "Orient Invoice"
				data.invoice_line_ids.price_unit = self.amt_total


# =================creating customer invoice on generate button=============================
# =================creating customer invoice on generate button=============================

	@api.multi
	def generate(self):

		data = self.env['account.invoice'].create({
				'partner_id':self.customer.id,
				'date_invoice':self.invoice_date,
				'bill_num':self.bl_number,
				'branch':self.branch.id,
				'summary_id': self.id

				})

		self.orient_link = data.id

		data.invoice_line_ids.create({
			'name':"Orient Invoice",
			'price_unit':self.amt_total,
			'account_id':17,
			'quantity':1,
			'invoice_id' : data.id

			})




class ufc_auto_tree(models.Model):
	_inherit = 'ufc.auto'

	orient_summary = fields.Many2one('orient.summ')