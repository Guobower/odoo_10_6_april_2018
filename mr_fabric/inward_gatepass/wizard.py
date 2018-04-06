from odoo import models, fields, api
from openerp.exceptions import Warning, ValidationError, UserError
import datetime
import datetime as dt
from odoo import exceptions, _


class InwardGatepassForm(models.Model):
	_name = "inward.gatepass"

	name = fields.Selection([
		('inwardgatepass','Inward Gatepass'),
		('outwardgatepass','Outward Gatepass'),
		],string='Type of Gatepass',required=True)

	stages = fields.Selection([
		('draft','Draft'),
		('validated','Validated'),
		],default="draft")

	sel = fields.Many2one('outward.type', string='Type')
	yarndyeing = fields.Many2one('yarn.dyeing',string='Yarn Dyeing')
	fabricdyeing = fields.Many2one('fabric.dyeing',string='Fabric Dyeing')
	fabricknitting = fields.Many2one('fabric.knitting',string='Fabric Knitting')
	to = fields.Char(string='Issue To/From')
	code = fields.Float(string='Code')
	return_able = fields.Char(string='Return able')
	category = fields.Many2one('outward.category',string='Category')
	store = fields.Char(string='Store')
	requesition = fields.Float(string='Requisition Code')
	issue_date =fields.Datetime(string='Issue Date')
	carrier = fields.Char(string='Carrier')
	vechicle = fields.Char(string='Vechicle No')
	status = fields.Char(string='Status')
	tree_link_id = fields.One2many('tree.link','tree_link')
	prepaid = fields.Many2one('hr.employee',string='Prepaid By:')
	approved = fields.Many2one('hr.employee',string='Approved By:')
						
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

class Treelink(models.Model):
	_name = 'tree.link'

	item = fields.Char(string='Item')
	quantity = fields.Float(string='Quantity')
	units = fields.Many2one('product.uom',string='Units')
	remarks = fields.Char(string='Remarks')
	tree_link = fields.Many2one('inward.gatepass')

class OutWardTypeClass(models.Model):
	_name = 'outward.type'

	name = fields.Char(string='Name')

class OutWardCategoryClass(models.Model):
	_name = 'outward.category'

	name = fields.Char(string='Name')