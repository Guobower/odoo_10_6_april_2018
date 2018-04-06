from odoo import models, fields, api
from openerp.exceptions import ValidationError 

class orient_bill_summary(models.Model):
	_name = 'orient.bills' 

	customer    = fields.Many2one('res.partner',string = "Customer")
	bl_number   = fields.Many2one('bill.num',string = "B/L Number")
	branch      = fields.Many2one('branch',string = "Branch")
	bill_no     = fields.Char(string = "Bill No")

# ================================getting branch of active user ==============================
# ================================getting branch of active user ==============================

	@api.onchange('customer')
	def get_branch(self):
		users = self.env['res.users'].search([('id','=',self._uid)])
		if self.customer:
			self.branch = users.Branch.id


# ====================punching data in orient summary on update button of wizard===============
# ====================punching data in orient summary on update button of wizard===============
	
	@api.multi
	def update(self):
		
		records = self.env['ufc.auto'].search([('customer.id','=',self.customer.id),('bl_number','=',self.bl_number.name)])

# ====================calculating total of sale price in orient_summary ======================
# ====================calculating total of sale price in orient_summary ======================

		company_tot = 0
		for data in records:
			print data.sale_price
			company_tot = company_tot + data.sale_price

# ====================validating data according to customer and b/l number======================
# ====================validating data according to customer and b/l number======================


		summ_model_recs = self.env['orient.summ'].search([])

		for data in summ_model_recs:
			if data.bl_number == self.bl_number.name:
				raise ValidationError("The record of this %s already exist" %self.bl_number.name)
		
			else:
				print "oooooooooooooooooooooooooooooo"


		create_reorder = self.env['orient.summ'].create({
			'customer':self.customer.id,
			'bl_number':self.bl_number.name,
			'branch':self.branch.id,
			'bill_no':self.bill_no,
			'amt_total':company_tot,
		})


		for y in records:
			y.orient_summary = create_reorder.id

