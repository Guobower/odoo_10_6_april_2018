from odoo import models, fields, api
from openerp.exceptions import ValidationError


class region_bill_summary(models.Model):
	_name = 'region.bills' 

	customer = fields.Many2one('res.partner',string = "Customer")
	branch   = fields.Many2one('branch',string = "Branch")
	form     = fields.Date(string="From")
	to       = fields.Date()
	bill_no  =fields.Char(string="Bill No")


	# =======================getting branch of active user=================================
	# =======================getting branch of active user=================================


	@api.onchange('customer')
	def get_branch(self):
		users = self.env['res.users'].search([('id','=',self._uid)])
		if self.customer:
			self.branch = users.Branch.id


	# ====================punching data in bill summary on update button of wizard==========
	# ====================punching data in bill summary on update button of wizard==========

	@api.multi
	def update(self):

		records = self.env['ufc.auto'].search([('customer.id','=',self.customer.id),('invoice_date','>=',self.form),('invoice_date','<=',self.to),('remaining','=',0)])
		entries = []
		for x in records:
			if x.region.code not in entries:
				entries.append(x.region.code)


	# ================punching bill num in preinvoices from wizard============================
	# ================punching bill num in preinvoices from wizard============================

		for line in records:
			line.Bill_No = self.bill_no


	# ================calculating total of amount in summary created by wizard==================
	# ================calculating total of amount in summary created by wizard==================

		def get_amt():
			active_ids = []
			grand_tot = 0
			for x in entries:

				del active_ids[:]

				for y in records:
					if y.region.code == x:
						active_ids.append(y)

				amount = 0
				for b in active_ids:
					amount = amount + b.sale_price

				grand_tot = grand_tot + amount

			return grand_tot
	

	# ========creating data in bill summary with validation on customer and dates============
	# ========creating data in bill summary with validation on customer and dates============



		summ_model_recs = self.env['summary.ffc'].search([])

		for data in summ_model_recs:
			if data.Customer.id == self.customer.id:
				if (data.date_from >= self.form and data.date_from <= self.to) or (data.date_to >= self.form and data.date_to <= self.to): 
					raise ValidationError("The record of this %s already exist" %self.customer.name)
		
			else:
				print "oooooooooooooooooooooooooooooo"


		create_reorder = self.env['summary.ffc'].create({
			'Customer':self.customer.id,
			'Branch':self.branch.id,
			'date_from':self.form,
			'date_to':self.to,
			'bill_no':self.bill_no,
			'amt_total': get_amt()
		})


		for y in records:
			y.ufc_summary = create_reorder.id

	
		for y in records:
			y.ufc_dharki = create_reorder.id
			
			
	# ==================calculating summary of records to punch in bill summary===============
	# ==================calculating summary of records to punch in bill summary===============


		active_ids = []
		grand_tot = 0
		for x in entries:

			del active_ids[:]

			for y in records:
				if y.region.code == x:
					active_ids.append(y)

			number_of_records = len(active_ids)/10
			sheets = number_of_records
			if number_of_records < 1:
				sheets = 1

			weight = 0
			for a in active_ids:
				weight = weight + int(a.weight)

			amount = 0
			for b in active_ids:
				amount = amount + b.sale_price

			grand_tot = grand_tot + amount

			region = ""
			for z in active_ids:
				region = z.region.name

			create_records = self.env['summary.tree'].create({
				'Region': x,
				'region_name': region,
				'sum_id': create_reorder.id,
				'Sheet': sheets,
				'M_tons': weight,
				'Amount': amount
		})

	

