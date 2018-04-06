# -*- coding: utf-8 -*- 
from odoo import models, fields, api
from openerp.exceptions import Warning, ValidationError, UserError
import datetime
import datetime as dt
from odoo import exceptions, _

class accessories(models.Model):
	_name = 'purchase.accessories'
	_order = 'id desc'
	_rec_name = 'sr_no'
	_inherit = ['mail.thread', 'ir.needaction_mixin']

	sr_no = fields.Char(string="Sr no")
	wonumber = fields.Many2many('mrp.production',string="WO No",)
	style = fields.Many2one('style.number',string="Style No")
	date = fields.Date(string="Date")
	merchant = fields.Many2one('hr.employee',string="Merchant")
	reference = fields.Many2one('purchase.accessories',string="Reference")

	vendor = fields.Many2one('res.partner',string="Vendor Name", required= True)

	customer = fields.Many2one('res.partner',string="Customer")
	delivery_date = fields.Date(string="Delivery Date")

	seq_code = fields.Char(string="Security Code")
	req_code = fields.Char(string="Req Code")
	
	accessories_stages = fields.Selection([
		('draft', 'Open'),
		('customer_approval', 'Customer Approval'),
		('validate', 'Validate'),
		],default='draft')

	picking_type_id = fields.Many2one('stock.picking.type',string="Picking Type")
	access_po_num = fields.Many2one('purchase.order',string="Po Num")

	tree_link = fields.One2many('purchase.accessories.tree','tree')

	@api.multi 
	def unlink(self): 
		for x in self: 
			if x.accessories_stages == "customer_approval" or x.accessories_stages == "validate" : 
				raise ValidationError('Cannot Delete Record') 
		return super(accessories,self).unlink()

	@api.onchange('sr_no','wonumber','style','date','merchant','vendor','customer','delivery_date','seq_code','req_code','access_po_num','tree_link')
	def picking_type(self):
		configuration = self.env['inventory.config'].search([])
		self.picking_type_id = configuration.access_order_config.id

	@api.model
	def create(self, vals):
		vals['sr_no'] = self.env['ir.sequence'].next_by_code('purchase.accessories')
		new_record = super(accessories, self).create(vals)

		return new_record
						
	@api.multi
	def in_draft(self):
		self.accessories_stages = "draft"

	@api.multi
	def in_customer_approval(self):
		self.accessories_stages = "customer_approval"

	@api.multi
	def in_rejected(self):
		self.accessories_stages = "rejected"

	@api.multi
	def in_approved(self):
		self.accessories_stages = "approved"

	@api.multi
	def in_validate(self):
		counter = 0
		approved = 0

		for x in self.tree_link:
			if (x.recieved != x.qty and x.recieved != 0 and x.recieved < x.qty) or x.approved == 'no':
				counter = counter + 1

		if counter == 0:
			self.create_stock_move()
			self.accessories_stages = "validate"

		else:
			return {
				'type': 'ir.actions.act_window',
				'name': 'Confirm Backorder',
				'res_model': 'accessories.wizard',
				'view_type': 'form',
				'view_mode': 'form',
				'target' : 'new',
				'context': {}
			}

	@api.multi
	def in_cancel(self):
		self.accessories_stages = "cancel"

	def create_stock_move(self):

		create_reorder = self.env['stock.picking'].create({
			'partner_id': self.vendor.id,
			'min_date': self.date,
			'origin': self.sr_no,
			'picking_type_id': self.picking_type_id.warehouse_id.id,
			'location_id': self.picking_type_id.default_location_src_id.id,
			'location_dest_id': self.picking_type_id.default_location_dest_id.id,
		})

		for x in self.tree_link:
			if x.approved == 'yes':
				total_quant = 0

				if x.recieved == 0:
					total_quant = x.qty
				else:
					total_quant = x.recieved

				create_variants = self.env['stock.move'].create({
					'product_id': x.product.id,
					'product_uom_qty': total_quant,
					'product_uom': x.unit_measurement.id,
					'picking_id': create_reorder.id,
					'location_id': create_reorder.location_id.id,
					'name': x.product.name,
					'location_dest_id': create_reorder.location_dest_id.id,
				})

		self.delivery = create_reorder.id

		create_reorder.action_assign()
		create_reorder.force_assign()

		stock = self.env['stock.picking'].search([('id','=',create_reorder.id)])

		for x in stock.pack_operation_product_ids:
			x.qty_done = x.product_qty

		create_reorder.do_new_transfer()

class accessories_tree(models.Model):
	_name = "purchase.accessories.tree"

	product = fields.Many2one('product.product',string="Product", required=True)
	unit_measurement = fields.Many2one('product.uom', string="Unit of Measurement")

	to_recieve = fields.Float(string="To Recieve")
	recieved = fields.Float(string="Recieved")
	rejected = fields.Float(string="Rejected")
	price = fields.Float(string="Unit Price")
	qty = fields.Float(string="Qty")
	sub_total = fields.Float(string="Amount")
	tree = fields.Many2one('purchase.accessories')
	yarn_tree = fields.Many2one('purchase.yarn')
	
	wo_no = fields.Many2one('mrp.production',string='WO No')
	buyer = fields.Many2one('res.partner',string='Buyer')

	remarks = fields.Char(string="Remarks")
	
	approved = fields.Selection([
		('yes', 'Yes'),
		('no', 'No'),
		],string="Approve")

	@api.onchange('price','qty')
	def sub_total_tree(self):
		self.sub_total = self.qty * self.price

	@api.onchange('product')
	def unit_tree(self):
		product = self.env['product.product'].search([('id','=',self.product.id)])
		self.unit_measurement = product.uom_id

class AccessoriesWizard(models.Model):
	_name = 'accessories.wizard'
	
	@api.multi
	def create_backorder(self):
		active_class = self.env['purchase.accessories'].browse(self._context.get('active_ids'))
		active_class.create_stock_move()

		count = 0
		create_access = self.env['purchase.accessories'].create({
			'style': active_class.style.id,
			'date': datetime.date.today(),
			'merchant': active_class.merchant.id,
			'vendor': active_class.vendor.id,
			'customer': active_class.customer.id,
			'delivery_date': active_class.delivery_date,
			'seq_code': active_class.seq_code,
			'req_code': active_class.req_code,
			'picking_type_id': active_class.picking_type_id.id,
			'access_po_num': active_class.access_po_num.id,
			'reference': active_class.id,
		})
		for work in active_class.wonumber:
			create_access.wonumber = create_access.wonumber + work 

		for x in active_class.tree_link:
			total_quant = 0

			if x.approved == 'no':
				total_quant = x.qty
			elif x.recieved == 0:
				total_quant = 0
			else:
				total_quant = x.qty - x.recieved

			if total_quant > 0:
				count = count + 1
				create_tree_variants = self.env['purchase.accessories.tree'].create({
					'product' : x.product.id,
					'unit_measurement' : x.unit_measurement.id,
					'qty' : total_quant,
					'tree': create_access.id
				})

		if count == 0:
			create_access.unlink()

		active_class.accessories_stages = "validate"

	@api.multi
	def no_backorder(self):
		active_class = self.env['purchase.accessories'].browse(self._context.get('active_ids'))
		active_class.create_stock_move()
		active_class.accessories_stages = "validate"

	@api.multi
	def cancel(self):
		print "----------------------------"

class yarn(models.Model):
	_name = 'purchase.yarn'
	_rec_name = 'sr_no'
	_inherit = ['mail.thread', 'ir.needaction_mixin']

	sr_no = fields.Char(string="Sr no")
	wonumber = fields.Char(string="WO No", required=True)
	style = fields.Char(string="Style No")
	date = fields.Date(string="Date")
	merchant = fields.Char(string="Merchant Name")
	amt_total = fields.Float(string="Amount Inc Tax",compute='total_tax',store=True)
	total = fields.Float(string="Amount",compute='total_tree',store=True)
	vendor = fields.Many2one('res.partner',string="Vendor Name", required= True)
	broker = fields.Many2one('res.partner',string="Broker")
	warehouse = fields.Many2one('stock.picking.type',string="Warehouse")
	destination_location = fields.Many2one('stock.location',string="Destination Location Zone")
	source_location = fields.Many2one('stock.location',string="Source Location Zone")
	delivery = fields.Many2one('stock.picking',string="Delivery")
	tax_id = fields.Many2one('account.tax',string="Tax")
	wo_num = fields.Many2one('mrp.production',string="WO#")

	tree_link = fields.One2many('purchase.accessories.tree','yarn_tree')

	@api.model
	def create(self, vals):
		vals['sr_no'] = self.env['ir.sequence'].next_by_code('purchase.yarn')
		new_record = super(yarn, self).create(vals)

		return new_record

	@api.depends('tree_link')
	def total_tree(self):
		self.total = 0.0
		for x in self.tree_link:
			self.total = x.sub_total + self.total

		self.total

	@api.depends('tax_id')
	def total_tax(self):
		if self.tax_id:
			value = self.total * self.tax_id.amount / 100
			self.amt_total = self.total + value

class yarnApproval(models.Model):
	_name = 'yarn.approval'
	_rec_name = 'date'
	_inherit = ['mail.thread', 'ir.needaction_mixin']

	date = fields.Date(string="Date")
	start_date = fields.Date(string="Start Date")
	end_date = fields.Date(string="End Date")

	won = fields.Many2one('mrp.production', string="Word order No.")
	yarn_count = fields.Many2one('product.product', string="Yarn Count")

	week = fields.Float(string="Week")

	tree_link = fields.One2many('yarn.requirement.tree','yarn_approval_tree')

	@api.multi
	def get_values(self):
		if self.tree_link:
			for x in self.tree_link:
				x.yarn_approval_tree = False

		require_lines = self.env['yarn.requirement.tree'].search([('approved','=',False)])
		records = []
		for x in require_lines:
			records.append(x)

		dates = []
		w_orders = []
		weeks = []
		products = []
		changes = 0

		if self.start_date and self.end_date:
			for x in records:
				if x.delv_date >= self.start_date and x.delv_date <= self.end_date:
					dates.append(x)
			++changes
		else:
			dates = records

		if self.won:
			for x in dates:
				if x.won.id == self.won.id:
					w_orders.append(x)
			++changes
		else:
			w_orders = dates
		
		if self.week:
			for x in w_orders:
				if x.week == self.week:
					weeks.append(x)
			++changes
		else:
			weeks = w_orders
		
		if self.yarn_count:
			for x in weeks:
				if x.product == self.yarn_count:
					products.append(x)
			++changes
		else:
			products = weeks

		if products == records and changes == 0:
			return
		else:
			for x in products:
				self.tree_link = self.tree_link + x

class YarnRequirement(models.Model):
	_name = "yarn.requirement"
	_rec_name = 'date'
	_inherit = ['mail.thread', 'ir.needaction_mixin']

	date = fields.Date("Date" ,required = True)
	won = fields.Many2many('mrp.production',string="Work Order No")
	stage = fields.Selection([('draft', 'Draft'),('val', 'Validate')],default = 'draft') 
	tree_link = fields.One2many('yarn.requirement.tree','yarn_tree')

	@api.multi 
	def unlink(self): 
		for x in self: 
			if x.stage == "val": 
				raise ValidationError('Cannot Delete Record') 
		return super(YarnRequirement,self).unlink()
	
	@api.multi
	def in_draft(self):
		self.stage = "draft"

	@api.multi
	def val(self):
		self.stage = "val"

		for x in self.tree_link:
			x.validated = True

	@api.multi
	def wait(self):
		self.stage = "wait"

	@api.multi
	def approve(self):
		self.stage = "approve"

	@api.multi
	def create_po(self):
		return {
			'type': 'ir.actions.act_window',
			'name': 'Create PO',
			'res_model': 'create.po.wizard',
			'view_type': 'form',
			'view_mode': 'form',
			'target' : 'new',
			'context': {'default_yarn_require':self.id,'default_get_val':True}
		}

	@api.multi
	def cancel(self):
		self.stage = "draft"

class CreatePoWizard(models.Model):
	_name = "create.po.wizard"

	yarn_require = fields.Many2one("yarn.requirement",string="Yarn")
	get_val = fields.Boolean(string="Get Values")

	tree_link = fields.One2many('yarn.requirement.tree','yarn_wizard_tree')

	@api.onchange('get_val')
	def get_values(self):
		rerquired = self.env['yarn.requirement'].search([('id','=',self.yarn_require.id)])

		for x in rerquired.tree_link:
			if x.approved == True and x.created == False:
				self.tree_link = self.tree_link + x

	@api.multi
	def create_po(self):
		active_class = self.env['purchase.order'].browse(self._context.get('active_ids'))

		rerquired = self.env['yarn.requirement.tree'].search([('yarn_tree.id','=',active_class.id,),('approved','=',True),('create_po','=',True),('created','=',False)])

		for x in rerquired:
			x.created = True

		brockers = []
		for x in rerquired:
			if x.broker not in brockers:
				brockers.append(x.broker)

		for x in brockers:
			print rerquired
			lines = []
			for r in rerquired:
				if r.broker.id == x.id:
					lines.append(r)

			create_order = self.env['purchase.order'].create({
				'partner_id': x.id,
				'ttype': "yarn",
				'date_order': datetime.date.today(),
			})

			for y in lines:

				lines = self.env['purchase.order.line'].create({
					'product_id' : y.product.id,
					'wo_no' : y.won.id,
					'product_qty' : y.qty,
					'measuring_unit' : y.measuring_unit,
					'nob' : y.nob,
					'no_kgs' : y.no_kgs,
					'price_unit' : y.unit_price,
					'product_uom': y.uom_id.id,
					'order_id': create_order.id,
					'name':  y.product.name,
					'date_planned': y.delv_date
				})
				create_order.wo_no = [(4,y.won.id)]
				create_order.date_planned = y.delv_date
				create_order.button_confirm()

	@api.multi
	def cancel(self):
		print "---------------------"

class YarnRequirementTree(models.Model):
	_name = "yarn.requirement.tree"
	_rec_name = "product"

	date = fields.Date(string="Date")
	product = fields.Many2one('product.product', string="Yarn Count", required=True)
	won = fields.Many2one('mrp.production',string="W/O")
	buyer = fields.Many2one('res.partner',string="Buyer")
	prod_type = fields.Many2one('product.product',string="Product Type")
	uom_id = fields.Many2one('product.uom',string="Product UOM")
	delv_date = fields.Date("Delivery Date")
	qty = fields.Float("Quantity")
	nob = fields.Float("No of Bags")
	lpp = fields.Float("Last Purchase Price")
	rate = fields.Many2many('yarn.rates',string="Rate")
	yarn = fields.Many2one('purchase.brand',string="Yarn Brand")
	appr_rate = fields.Many2one('yarn.rates',string="Approved Rate")
	unit_price = fields.Float("Unit Price")
	week = fields.Float("Week")
	broker = fields.Many2one('res.partner',string="Broker")

	approved = fields.Boolean(string="Approved")
	created = fields.Boolean(string="Po Created")
	create_po = fields.Boolean(string="Create Po")
	validated = fields.Boolean(string="Validated")

	yarn_tree = fields.Many2one('yarn.requirement')
	yarn_approval_tree = fields.Many2one('yarn.approval')
	yarn_wizard_tree = fields.Many2one('create.po.wizard')

	no_kgs = fields.Float("No of KGs")
	
	measuring_unit = fields.Selection([
		('bags', 'Bags'),
		('kgs', 'KGs'),
		],default='kgs', string="UOM")

	@api.onchange('product','won','buyer','prod_type','delv_date','qty','nob','lpp','rate','yarn')
	def date_change(self):
		self.date = self.yarn_tree.date

	@api.onchange('appr_rate')
	def appr_rate_change(self):
		self.unit_price = self.appr_rate.name

	@api.onchange('measuring_unit')
	def appr_unit_change(self):
		if self.measuring_unit:

			if self.measuring_unit == 'bags':
				units = self.env['product.uom'].search([('name','=','bag')])
				self.uom_id = units.id

			if self.measuring_unit == 'kgs':
				units = self.env['product.uom'].search([('name','=','kg')])
				self.uom_id = units.id

	@api.onchange('won')
	def won_change(self):
		buyers = []
		work_order = self.env['mrp.production'].search([('id','=',self.won.id)])

		self.buyer = work_order.buyer.id
		self.prod_type = work_order.product.id
		self.delv_date = work_order.delivery

	@api.onchange('delv_date')
	def delivery(self):
		if self.delv_date:

			myDateTime = dt.datetime.strptime(self.delv_date,'%Y-%m-%d')
			yr,weekNumber,weekDay = myDateTime.isocalendar()
			self.week = weekNumber

	@api.multi
	def approve_line(self):
		if self.appr_rate:
			self.approved = "True"
		else:
			return {'value':{}, 'warning':{
			'title': 'Warning', 'message': 'Please Approve any Rate First.'}}

	@api.onchange('appr_rate')
	def get_rates(self):
		self.broker = self.appr_rate.partner.id
		self.unit_price = self.appr_rate.name

	@api.onchange('qty')
	def qty_change(self):
		if self.measuring_unit == 'bags':
			if self.qty:
				self.nob = self.qty
				if self.product.net_weight:
					self.no_kgs = self.nob * self.product.net_weight

		
		if self.measuring_unit == 'kgs':
			if self.qty:
				self.no_kgs = self.qty
				if self.product.net_weight:
					self.nob = self.no_kgs / self.product.net_weight

class YarnRate(models.Model):
	_name = "yarn.rates"
	_rec_name = 'rec'

	name = fields.Char("Rate" ,required=True)
	rec = fields.Char("rec")
	partner = fields.Many2one('res.partner',string="Broker",required=True)
	yarn = fields.Many2one('purchase.brand',string="Yarn Brand")
	@api.onchange('name','partner','yarn')
	def name_partner(self):
		if self.name:
			self.rec = "%s %s %s %s %s" %(self.partner.name or ''," ", self.yarn.name or ''," ", self.name or '')

class PurchaseOrderExt(models.Model):
	_inherit = 'purchase.order'

	wo_no = fields.Many2many('mrp.production',string='WO No',required = True)
	date_planned = fields.Datetime(string="Current Date")
	style = fields.Many2one('style.number',string="Style No")
	merchant = fields.Many2one('hr.employee',string="Merchant")
	order_line2 = fields.One2many('purchase.order.line','order_id')
	purchase_recharge_count = fields.Integer(string="Recharge",compute='act_show_accessories_deliveries')
	ttype = fields.Selection([
		('yarn', 'Yarn'),
		('fabric', 'Fabric'),
		('accessories', 'Accessories'),
		('general', 'General')
		],default='yarn', required=True, string="Type")

	@api.multi
	def custom_button(self):

		prev_order = self.env['purchase.accessories'].search([('access_po_num','=',self.id)])

		if prev_order:
			raise ValidationError("Accessories Order against this PO already Exist")

		else:

			configuration = self.env['inventory.config'].search([])

			purchase_accessories_env=self.env['purchase.accessories']
			purchase_accessories_record=purchase_accessories_env.create({
				'vendor' : self.partner_id.id,
				'access_po_num' : self.id,
				'style': self.style.id,
				'date': self.date_order,
				'merchant': self.merchant.id,
				'delivery_date': self.date_planned,
				'picking_type_id': configuration.access_order_config.id
				})

			for x in self.order_line:
				lines=self.env['purchase.accessories.tree'].create({
				'product' : x.product_id.id,
				'unit_measurement' : x.product_uom.id,
				'wo_no' : x.wo_no.id,
				'buyer' : x.buyer.id,
				'qty' : x.product_qty,
				'to_recieve' : x.product_qty,
				'price' : x.price_unit,
				'tree' : purchase_accessories_record.id,
				})

			for work in self.wo_no:
				purchase_accessories_record.wonumber = purchase_accessories_record.wonumber + work

			self.state = "purchase"

	@api.one 
	def act_show_accessories_deliveries(self):

		self.purchase_recharge_count = self.env['purchase.accessories'].search_count([('access_po_num','=',self.id)])

	@api.onchange('order_line')
	def line_change(self):

		total = 0
		taxes = 0
		for x in self.order_line:
			total = total + x.price_subtotal
			for tax in x.taxes_id:
				taxed = (x.price_subtotal * tax.amount)/100
				taxes = taxes + taxed

		self.amount_untaxed = total
		self.amount_tax = taxes

		self.amount_total = self.amount_untaxed + self.amount_tax


	@api.onchange('partner_id')
	def _date_planned(self):
		self.date_planned = datetime.date.today()

	@api.onchange('order_line2')
	def line_change2(self):
		total = 0
		taxes = 0
		for x in self.order_line2:
			total = total + x.price_subtotal
			for tax in x.taxes_id:
				taxed = (x.price_subtotal * tax.amount)/100
				taxes = taxes + taxed

		self.amount_untaxed = total
		self.amount_tax = taxes

		self.amount_total = self.amount_untaxed + self.amount_tax

	@api.onchange('wo_no','partner_id')
	def get_picking_type(self):
		if self.ttype == 'yarn':
			setting = self.env['inventory.config'].search([])
			self.picking_type_id = setting.yarn_po_config.id

class PurchaseOrderLineExt(models.Model):
	_inherit = 'purchase.order.line'

	nob = fields.Float("No of Bags")
	no_kgs = fields.Float("No of KGs")
	wo_no = fields.Many2one('mrp.production',string='WO No')
	buyer = fields.Many2one('res.partner',string='Buyer')
	product_id = fields.Many2one('product.product',string='Product',options="{'no_create': True, 'no_create_edit':True}")
	
	measuring_unit = fields.Selection([
		('bags', 'Bags'),
		('kgs', 'KGs'),
		],default='kgs', string="Unit of Measurement")

	@api.onchange('product_qty')
	def qty_change(self):
		if self.measuring_unit == 'bags':
			if self.product_qty:
				self.nob = self.product_qty
				if self.product_id.net_weight:
					self.no_kgs = self.nob * self.product_id.net_weight

		
		if self.measuring_unit == 'kgs':
			if self.product_qty:
				self.no_kgs = self.product_qty
				if self.product_id.net_weight:
					self.nob = self.no_kgs / self.product_id.net_weight

	@api.onchange('product_id')
	def line_change(self):
		if not self.order_id.wo_no:
			raise exceptions.except_orm(_('Error'), _('Please Select Work Order Number first.'))

	@api.onchange('wo_no')
	def line_change(self):
		w_order = self.env['mrp.production'].search([('id','=',self.wo_no.id)])
		self.buyer = w_order.buyer.id

class StockPickingExt(models.Model):
	_inherit = 'stock.picking'

	req_code = fields.Char("Requisition Code")
	sec_code = fields.Char("Security Code")

class YarnDyeing(models.Model):
	_name = "yarn.dyeing"
	_inherit = ['mail.thread', 'ir.needaction_mixin']

	name = fields.Many2one('res.partner',string="To")
	date = fields.Date(" Start Date")
	c_date = fields.Date("Completion Date")
	buyer = fields.Many2many('res.partner',string="Buyer")
	style = fields.Many2many('style.number',string="Style No")
	won = fields.Many2many('mrp.production',string="Work Order No", required= True)
	delv_date = fields.Date("Delivery Date")
	plan_date = fields.Date("Plan Date")
	primary = fields.Many2one('purchase.primary', string="Primary")
	secondary = fields.Many2one('purchase.secondary', string = "Secondary")
	des = fields.Text("Note")
	mf = fields.Char("MF No")
	req_code = fields.Char("Requisition Code")
	sec_code = fields.Char("Security Code")
	tree_link = fields.One2many('yarn.dyeing.tree','yarn_tree')
	recharge_count = fields.Integer(string="Recharge", compute="_load_list")
	least_wastage = fields.Float(string='Least Wastage',default=2)

	picking_type_id = fields.Many2one('stock.picking.type',string="Picking Type")
	scrap_type_id = fields.Many2one('stock.picking.type',string="Scrap Move")

	stage = fields.Selection([('draft', 'Draft'),
		('sent', 'Sent'),
		('complete', 'Complete')
		],default = 'draft')

	@api.multi 
	def unlink(self): 
		for x in self: 
			if x.stage == "sent" or x.stage == "complete" : 
				raise ValidationError('Cannot Delete Record') 
		return super(YarnDyeing,self).unlink()

	@api.onchange('name','won')
	def get_picking_type_id(self):
		setting = self.env['inventory.config'].search([])
		self.scrap_type_id = setting.yarn_dying_config_scrap.id
		# self.picking_type_id = setting.yarn_dying_config.id

	@api.one
	def _load_list(self):
		self.recharge_count = self.env['yarn.wizard.class'].search_count([('tree_id','=',self.id)])

	@api.onchange('won')
	def get_buyer(self):
		buyers = []
		styles = []
		for x in self.won:
			work_order = self.env['mrp.production'].search([('id','=',x.id)])
			
			if work_order.delivery:
				self.delv_date = work_order.delivery
			
			if work_order.buyer:
				if work_order.buyer.id not in buyers:
					buyers.append(work_order.buyer.id)
			
			if work_order.style_no:
				if work_order.style_no.id not in styles:
					styles.append(work_order.style_no.id)

		self.buyer = buyers
		self.style = styles

	@api.multi
	def in_draft(self):
		self.stage = "draft"

		tree_recs = self.env['yarn.dyeing.tree'].search([('yarn_tree.id','=',self.id)])
		if tree_recs:
			for x in tree_recs:
				x.stageed = self.stage

	@api.multi
	def in_sent(self):
		self.stage = "sent"

		inventory = self.env['stock.picking']
		inventory_lines = self.env['stock.move'].search([])
		create_inventory = inventory.create({
			'partner_id':self.name.id,
			'location_id': self.picking_type_id.default_location_src_id.id,
			'picking_type_id' : self.picking_type_id.id,
			'location_dest_id' : self.picking_type_id.default_location_dest_id.id,
			'origin': 'Yarn Dyeing',
		})

		for x in self.tree_link:
			create_inventory_lines = inventory_lines.create({
				'product_id':x.yarn.id,
				'product_uom_qty':x.issue_qty,
				'product_uom': x.yarn.uom_id.id,
				'location_id':15,
				'picking_id': create_inventory.id,
				'name':"test",
				'location_dest_id': 9,
				})

		self.delivery = create_inventory.id

		create_inventory.action_assign()
		create_inventory.force_assign()

		stock = self.env['stock.picking'].search([('id','=',create_inventory.id)])

		for x in stock.pack_operation_product_ids:
			x.qty_done = x.product_qty

		create_inventory.do_new_transfer()

		tree_recs = self.env['yarn.dyeing.tree'].search([('yarn_tree.id','=',self.id)])

		if tree_recs:
			for x in tree_recs:
				x.stageed = self.stage

	@api.multi
	def complete(self):

		count = 0
		for x in self.tree_link:
			if x.stage != 'done':
				count = count + 1

		print count

		if count == 0:

			inventory = self.env['stock.picking']
			inventory_lines = self.env['stock.move'].search([])
			create_inventory = inventory.create({
				'partner_id':self.name.id,
				'location_id': self.scrap_type_id.default_location_src_id.id,
				'picking_type_id' : self.scrap_type_id.id,
				'location_dest_id' : self.scrap_type_id.default_location_dest_id.id,
				'origin': 'Yarn Dyeing Scrap',
			})

			for x in self.tree_link:
				create_inventory_lines = inventory_lines.create({
					'product_id':x.yarn.id,
					'product_uom_qty': (x.issue_qty - x.receive_qty),
					'product_uom': x.yarn.uom_id.id,
					'location_id':15,
					'picking_id': create_inventory.id,
					'name':"test",
					'location_dest_id': 9,
					})

			self.delivery = create_inventory.id

			create_inventory.action_assign()
			create_inventory.force_assign()

			stock = self.env['stock.picking'].search([('id','=',create_inventory.id)])

			for x in stock.pack_operation_product_ids:
				x.qty_done = x.product_qty

			create_inventory.do_new_transfer()
			self.stage = "complete"

		elif count != 0:
			raise exceptions.except_orm(_('Error'), _('Recived Quantity should not be greater than the Reciveable Quantity'))

		tree_recs = self.env['yarn.dyeing.tree'].search([('yarn_tree.id','=',self.id)])

		if tree_recs:
			for x in tree_recs:
				x.stageed = self.stage

	@api.multi
	def yarn_receiving(self):
		return {
		'type': 'ir.actions.act_window',
		'name': 'Yarn Receiving',
		'res_model': 'yarn.wizard.class',
		'view_type': 'form',
		'view_mode': 'form',
		'context': {'default_get_list': True,'readonly_by_pass': True},
		}

class YarnDyeingTree(models.Model):
	_name = "yarn.dyeing.tree"

	won = fields.Many2one('mrp.production',string="W/O",required = True)
	color = fields.Many2one('purchase.color',string="Colors")
	yarn = fields.Many2one('product.product',string="Yarn Count")
	lot = fields.Char(string="Lot No")
	rate = fields.Float(string="Rate")
	issue_qty = fields.Float(string="Issue Qty")
	receive_qty = fields.Float(string="Received Qty (Kg)")
	receiveable_qty = fields.Float(string="Receivable Qty (Kg)")
	blc = fields.Char(string="Balance" ,compute='_blc')
	wastage = fields.Char(string="Actual Wastage" ,compute='_wastage')
	agree_wastage = fields.Float(string="Agreed Wastage")
	std = fields.Binary(string="STD")
	yarn_tree = fields.Many2one('yarn.dyeing')

	stage = fields.Selection([
		('inprogress', 'In Progress'),
		('done', 'Done'),
		],default = 'inprogress')

	stageed = fields.Selection([
		('draft', 'Draft'),
		('sent', 'Sent'),
		('in_house', 'In House'),
		('complete', 'Complete')
		],default = 'draft')
	
	@api.one
	@api.depends('receiveable_qty','receive_qty')
	def _blc(self):
		balance = self.receive_qty - self.receiveable_qty
		if balance < 0:
			self.blc = balance
		if balance > 0:
			self.blc = "+" + str(balance)

	@api.one
	@api.depends('issue_qty','blc')
	def _wastage(self):
		if self.issue_qty:
			if self.blc:
				waste = ((float(self.blc) / self.issue_qty)* 100)
				if waste < 0:
					self.wastage = str("{0:.2f}".format(waste * (-1))) + "%"
				if waste > 0:
					self.wastage = str("{0:.2f}".format(waste)) + "%"   

	@api.onchange('issue_qty','agree_wastage')
	def get_recivable(self):
		if self.issue_qty > 0.0:
			self.receiveable_qty = self.issue_qty - ((self.agree_wastage * self.issue_qty)/ 100)

	@api.onchange('receive_qty')
	def get_recived(self):
		recived = self.receive_qty
		reciveable = self.receiveable_qty + (self.receiveable_qty*0.1)
		if recived > reciveable:
			self.receive_qty = self.receiveable_qty
			return {'value':{}, 'warning':{
			'title': 'Warning', 'message': 'Recived Quantity should not be greater than the Reciveable Quantity'}}

class Yarn_Receiving_Wizard(models.Model):
	_name = "yarn.wizard.class"
	_rec_name = 'id'

	yarn_link  = fields.One2many("yarn.wizard.tree","yarn_tree")
	get_list = fields.Boolean("Get List")
	l_list = fields.Boolean("L List")
	tree_id = fields.Integer("ID")
	date = fields.Date("Date" ,required=True)
	name = fields.Many2one('res.partner',string="Name")
	mf_no = fields.Char("MF No")
	seq_code = fields.Char("Security Code")
	req_code = fields.Char("Requisition Code")
	least_wastage = fields.Float(string='Least Wastage')

	picking_type_id = fields.Many2one('stock.picking.type',string="Picking Type")
	
	stage = fields.Selection([
		('draft', 'Draft'),
		('validate', 'Validate'),
		],default="draft")

	@api.onchange('get_list')
	def get_lines(self):
 
		active_class = self.env['yarn.dyeing'].browse(self._context.get('active_id'))
		data = []
		t = 0.0
		if self.get_list == True:
			self.tree_id = active_class.id
			self.name = active_class.name
			self.least_wastage = active_class.least_wastage
			for x in active_class.tree_link:
				if x.stage != 'done':
					if x.receive_qty > 0:
						t = x.receiveable_qty - x.receive_qty
					else:
						t = x.receiveable_qty
					data.append({
						'fr_won':x.won,
						'fr_lot':x.lot,
						'fr_todo':t,
						'color':x.color.id,
						'yarn_count': x.yarn.id,
						})
			self.yarn_link = data
			self.picking_type_id = active_class.picking_type_id
			self.mf_no = active_class.mf

	@api.multi
	def update(self):
		active_class = self.env['yarn.dyeing'].browse(self._context.get('active_id'))
		if active_class:
			self.tree_id = active_class.id
			for x in self.yarn_link:
				if x.fr_done > 0:
					for y in active_class.tree_link:
						estimated_val = 0
						if x.fr_won == y.won and y.yarn.id == x.yarn_count.id:
							y.lot = x.fr_lot
							y.receive_qty = x.fr_done + y.receive_qty

							estimated_val = y.receiveable_qty - ((y.receiveable_qty*self.least_wastage)/100)
							if y.receive_qty >= estimated_val:
								y.stage = 'done'

							self.l_list = 'True'

		inventory = self.env['stock.picking']
		inventory_lines = self.env['stock.move'].search([])
		create_inventory = inventory.create({
			'partner_id':self.name.id,
			'location_id': self.picking_type_id.default_location_dest_id.id,
			'picking_type_id' : self.picking_type_id.id,
			'location_dest_id' : self.picking_type_id.default_location_src_id.id,
			'origin': 'Yarn Reciving',
		})

		for x in self.yarn_link:
			create_inventory_lines = inventory_lines.create({
				'product_id':x.yarn_count.id,
				'product_uom_qty':x.fr_done,
				'product_uom': x.yarn_count.uom_id.id,
				'location_id':15,
				'picking_id': create_inventory.id,
				'name':"test",
				'location_dest_id': 9,
				})

		self.delivery = create_inventory.id

		create_inventory.action_assign()
		create_inventory.force_assign()

		stock = self.env['stock.picking'].search([('id','=',create_inventory.id)])

		for x in stock.pack_operation_product_ids:
			x.qty_done = x.product_qty

		create_inventory.do_new_transfer()
		self.stage = "validate"

class Yarn_Receiving_Wizard_Tree(models.Model):
	_name="yarn.wizard.tree"

	fr_won = fields.Many2one('mrp.production',string="W/O",required = True)
	fr_lot = fields.Char(string="Lot No")
	fr_todo = fields.Float("To Do")
	fr_done = fields.Float("Done")
	yarn_tree = fields.Many2one("yarn.wizard.class")
	color = fields.Many2one('purchase.color',string="Color")
	yarn_count = fields.Many2one('product.product',string="Yarn Count")

	@api.onchange('fr_done')
	def get_yarn_done(self):
		recived = self.fr_done
		reciveable = self.fr_todo + (self.fr_todo*0.1)

		if recived > reciveable:
			self.fr_done = self.fr_todo
			return {'value':{}, 'warning':{
			'title': 'Warning', 'message': 'Recived Quantity should not be greater than the Reciveable Quantity'}}

class FabricDyeing(models.Model):
	_name = "fabric.dyeing"
	_inherit = ['mail.thread', 'ir.needaction_mixin']

	name = fields.Many2one('res.partner',string="To")
	date = fields.Date("Start Date")
	c_date = fields.Date("Completion Date")
	subject = fields.Char("Subject")
	buyer = fields.Many2many('res.partner',string="Buyer")
	style = fields.Many2many('style.number',string="Style No")
	won = fields.Many2many('mrp.production',string="Work Order No", required=True)
	delv_date = fields.Date("Delivery Date")
	plan_date = fields.Date("Plan Date")
	primary = fields.Many2one('purchase.primary', string="Primary")
	secondary = fields.Many2one('purchase.secondary', string = "Secondary")
	des = fields.Text("Note")
	req_code = fields.Char("Requisition Code")
	sec_code = fields.Char("Security Code")
	tree_link = fields.One2many('fabric.dyeing.tree','yarn_tree')
	recharge_count = fields.Integer(string="Recharge", compute="_load_list")
	least_wastage = fields.Float(string='Least Wastage',default=2)

	stage = fields.Selection([('draft', 'Draft'),
		('sent', 'Sent'),
		('complete', 'Complete')
		],default = 'draft') 

	picking_type_id = fields.Many2one('stock.picking.type',string="Picking Type")
	scrap_move = fields.Many2one('stock.picking.type',string="Scrap move")

	@api.multi 
	def unlink(self): 
		for x in self: 
			if x.stage == "sent" or x.stage == "complete" : 
				raise ValidationError('Cannot Delete Record') 
		return super(FabricDyeing,self).unlink()

	@api.onchange('won')
	def get_buyer(self):
		buyers = []
		styles = []
		for x in self.won:
			work_order = self.env['mrp.production'].search([('id','=',x.id)])
			
			if work_order.delivery:
				self.delv_date = work_order.delivery
			
			if work_order.buyer:
				if work_order.buyer.id not in buyers:
					buyers.append(work_order.buyer.id)
			
			if work_order.style_no:
				if work_order.style_no.id not in styles:
					styles.append(work_order.style_no.id)

		self.buyer = buyers
		self.style = styles

	@api.onchange('name','won')
	def get_picking_type_id(self):
		setting = self.env['inventory.config'].search([])
		self.scrap_move = setting.fabric_dying_config_scrap.id
		# self.picking_type_id = setting.fabric_dying_config.id

	@api.one
	def _load_list(self):
		self.recharge_count = self.env['fabric.wizard.class'].search_count([('tree_id','=',self.id)])

	@api.multi
	def in_draft(self):
		self.stage = "draft"

		tree_recs = self.env['fabric.dyeing.tree'].search([('yarn_tree.id','=',self.id)])
		if tree_recs:
			for x in tree_recs:
				x.stageed = self.stage

	@api.multi
	def in_sent(self):
		self.stage = "sent"

		inventory = self.env['stock.picking']
		inventory_lines = self.env['stock.move'].search([])
		create_inventory = inventory.create({
			'partner_id':self.name.id,
			'location_id': self.picking_type_id.default_location_src_id.id,
			'picking_type_id' : self.picking_type_id.id,
			'location_dest_id' : self.picking_type_id.default_location_dest_id.id,
			'origin': 'Fabric Dyeing',
		})

		for x in self.tree_link:
			create_inventory_lines = inventory_lines.create({
				'product_id':x.fabric.id,
				'product_uom_qty':x.issue_qty,
				'product_uom': x.fabric.uom_id.id,
				'location_id':15,
				'picking_id': create_inventory.id,
				'name':"test",
				'location_dest_id': 9,
				})

		self.delivery = create_inventory.id

		create_inventory.action_assign()
		create_inventory.force_assign()

		stock = self.env['stock.picking'].search([('id','=',create_inventory.id)])

		for x in stock.pack_operation_product_ids:
			x.qty_done = x.product_qty

		create_inventory.do_new_transfer()

		tree_recs = self.env['fabric.dyeing.tree'].search([('yarn_tree.id','=',self.id)])
		if tree_recs:
			for x in tree_recs:
				x.stageed = self.stage

	@api.multi
	def in_complete(self):

		inventory = self.env['stock.picking']
		inventory_lines = self.env['stock.move'].search([])
		create_inventory = inventory.create({
			'partner_id':self.name.id,
			'location_id': self.scrap_move.default_location_src_id.id,
			'picking_type_id' : self.scrap_move.id,
			'location_dest_id' : self.scrap_move.default_location_dest_id.id,
			'origin': 'Fabric Dyeing Scrap',
		})

		for x in self.tree_link:
			create_inventory_lines = inventory_lines.create({
				'product_id':x.fabric.id,
				'product_uom_qty': (x.issue_qty - x.receive_qty),
				'product_uom': x.fabric.uom_id.id,
				'location_id':15,
				'picking_id': create_inventory.id,
				'name':"test",
				'location_dest_id': 9,
				})

		self.delivery = create_inventory.id

		create_inventory.action_assign()
		create_inventory.force_assign()

		stock = self.env['stock.picking'].search([('id','=',create_inventory.id)])

		for x in stock.pack_operation_product_ids:
			x.qty_done = x.product_qty

		create_inventory.do_new_transfer()
		self.stage = "complete"

		tree_recs = self.env['fabric.dyeing.tree'].search([('yarn_tree.id','=',self.id)])
		if tree_recs:
			for x in tree_recs:
				x.stageed = self.stage

	@api.multi
	def fabric_receiving(self):

		return {
			'type': 'ir.actions.act_window',
			'name': 'Fabric Receiving',
			'res_model': 'fabric.wizard.class',
			'view_type': 'form',
			'view_mode': 'form',
			'context': {'fabric_no':self.id,'default_get_list': True,'readonly_by_pass': True},
		}

class FabricDyeingTree(models.Model):
	_name = "fabric.dyeing.tree"

	won = fields.Many2one('mrp.production',string="W/O",required = True)
	color = fields.Many2one('purchase.color',string="Colors")
	lot = fields.Char(string="Lot No")
	fabric = fields.Many2one('product.product',string="Fabric")
	dia = fields.Many2one('purchase.dia' , string="Dia")
	gauge = fields.Many2one('purchase.gauge' , string="Gauge")
	ndl = fields.Many2one('purchase.ndl' , string="NDL")
	width = fields.Many2one('purchase.width' , string="Width")
	gsm = fields.Many2one('purchase.gsm' , string="GSM")
	process = fields.Many2one('purchase.process' , string="Process")
	rate = fields.Float("Rate")
	issue_qty = fields.Float("Issue Qty")
	receive_qty = fields.Float("Received Qty (Kg)")
	receivable_qty = fields.Float("Receivable Qty (Kg)")
	blc = fields.Float("Balance" ,compute='_blc')
	wastage = fields.Char("Actual Wastage" ,compute='_wastage', digits=(16,2))
	descrip = fields.Char("Accessories Description")
	agree_wastage = fields.Float(string="Agreed Wastage")
	yarn_tree = fields.Many2one('fabric.dyeing')
	
	accessories = fields.Selection([
		('collar', 'Collar'),
		('cuff', 'Cuff'),
		('draw_cord', 'Draw Cord'),
		('tape', 'Tape'),
		],default="collar",string="Accessories")

	stage = fields.Selection([
		('inprogress', 'In Progress'),
		('done', 'Done'),
		],default = 'inprogress')

	stageed = fields.Selection([
		('draft', 'Draft'),
		('sent', 'Sent'),
		('in_house', 'In House'),
		('complete', 'Complete')
		],default = 'draft')

	@api.one
	@api.depends('receivable_qty','receive_qty')
	def _blc(self):
		balance = self.receive_qty - self.receivable_qty
		if balance < 0:
			self.blc = balance
		if balance > 0:
			self.blc = "+" + str(balance)

	@api.one
	@api.depends('issue_qty','blc')
	def _wastage(self):
		if self.issue_qty:
			if self.blc:
				waste = ((self.blc / self.issue_qty)* 100)
				if waste < 0:
					self.wastage = str("{0:.2f}".format(waste * (-1))) + "%"
				if waste > 0:
					self.wastage = str("{0:.2f}".format(waste)) + "%"

	@api.onchange('issue_qty','agree_wastage')
	def get_reciveable(self):
		if self.issue_qty > 0.0:
			self.receivable_qty = self.issue_qty - ((self.agree_wastage * self.issue_qty)/ 100)

	@api.onchange('receive_qty')
	def get_recived(self):
		recived = self.receive_qty
		reciveable = self.receivable_qty + (self.receivable_qty*0.1)
		if recived > reciveable:
			self.receive_qty = self.receivable_qty
			return {'value':{}, 'warning':{
			'title': 'Warning', 'message': 'Recived Quantity should not be greater than the Reciveable Quantity'}}

class Fabric_Receiving_Wizard(models.Model):
	_name = "fabric.wizard.class"
	_rec_name = 'id'

	fabric_link  = fields.One2many("fabric.wizard.tree","fabric_tree")
	get_list = fields.Boolean("Get List")
	l_list = fields.Boolean("L List")
	tree_id = fields.Integer("ID")
	date = fields.Date("Date" ,required=True)
	name = fields.Many2one('res.partner',string="Name")
	seq_code = fields.Char("Security Code")
	req_code = fields.Char("Requisition Code")
	least_wastage = fields.Float(string='Least Wastage')

	picking_type_id = fields.Many2one('stock.picking.type',string="Picking Type")
	
	stage = fields.Selection([
		('draft', 'Draft'),
		('validate', 'Validate'),
		],default="draft")

	@api.onchange('get_list')
	def get_lines(self):
 
		active_class = self.env['fabric.dyeing'].browse(self._context.get('active_id'))
		data = []
		t = 0.0
		if self.get_list == True:
			self.tree_id = active_class.id
			self.name = active_class.name
			self.least_wastage =  active_class.least_wastage

			for x in active_class.tree_link:
				if x.stage != 'done':
					if x.receive_qty > 0:
						t = x.receivable_qty - x.receive_qty
					else:
						t = x.receivable_qty
					data.append({
						'fr_won':x.won,
						'fr_lot':x.lot,
						'fr_todo':t,
						'color': x.color.id,
						'yarn_count': x.fabric.id,
						})
			self.fabric_link = data
			self.picking_type_id = active_class.picking_type_id

	@api.multi
	def update(self):
		active_class = self.env['fabric.dyeing'].browse(self._context.get('active_id'))
		if active_class:
			self.tree_id = active_class.id
			for x in self.fabric_link:
				estimated_val = 0
				if x.fr_done > 0:
					for y in active_class.tree_link:
						if x.fr_won == y.won and x.yarn_count.id == y.fabric.id:
							y.receive_qty = x.fr_done + y.receive_qty

							estimated_val = y.receivable_qty - ((y.receivable_qty*self.least_wastage)/100)
							if y.receive_qty >= estimated_val:
								y.stage = 'done'

							self.l_list = 'True'

		inventory = self.env['stock.picking']
		inventory_lines = self.env['stock.move'].search([])
		create_inventory = inventory.create({
			'partner_id':self.name.id,
			'location_id': self.picking_type_id.default_location_dest_id.id,
			'picking_type_id' : self.picking_type_id.id,
			'location_dest_id' : self.picking_type_id.default_location_src_id.id,
			'origin': 'Fabric Reciving',
		})

		for x in self.fabric_link:
			if x.fr_done > 0:
				create_inventory_lines = inventory_lines.create({
					'product_id':x.yarn_count.id,
					'product_uom_qty':x.fr_done,
					'product_uom': x.yarn_count.uom_id.id,
					'location_id':15,
					'picking_id': create_inventory.id,
					'name':"test",
					'location_dest_id': 9,
					})

		self.delivery = create_inventory.id

		create_inventory.action_assign()
		create_inventory.force_assign()

		stock = self.env['stock.picking'].search([('id','=',create_inventory.id)])

		for x in stock.pack_operation_product_ids:
			x.qty_done = x.product_qty

		create_inventory.do_new_transfer()
		self.stage = "validate"

class Fabric_Receiving_Wizard_Tree(models.Model):
	_name="fabric.wizard.tree"

	fr_won = fields.Many2one('mrp.production',string="W/O",required = True)
	fr_lot = fields.Char(string="Lot No")
	fr_todo = fields.Float("To Do")
	fr_done = fields.Float("Done")
	fabric_tree = fields.Many2one("fabric.wizard.class")
	color = fields.Many2one('purchase.color',string="Color")
	yarn_count = fields.Many2one('product.product',"Yarn Count")

	@api.onchange('fr_done')
	def get_fab_done(self):
		recived = self.fr_done
		reciveable = self.fr_todo + (self.fr_todo*0.1)

		if recived > reciveable:
			self.fr_done = self.fr_todo
			return {'value':{}, 'warning':{
			'title': 'Warning', 'message': 'Recived Quantity should not be greater than the Reciveable Quantity'}}

class FabricKnitting(models.Model):
	_name = "fabric.knitting"
	_inherit = ['mail.thread', 'ir.needaction_mixin']

	name = fields.Many2one('res.partner',string="To")
	date = fields.Date("Order Date" , required=True)
	buyer = fields.Many2many('res.partner',string="Buyer")
	won = fields.Many2many('mrp.production',string="W/O")
	delv_date = fields.Date("Delivery Date")
	c_date = fields.Date("Order Completion Date")
	plan_date = fields.Date("Plan Date")
	style = fields.Many2many('style.number',string="Style No")
	req_code = fields.Char("Requisition Code")
	sec_code = fields.Char("Security Code")
	tree_link = fields.One2many('fabric.knitting.tree','fabric_tree')
	recharge_count = fields.Integer(string="Recharge", compute="_load_list")
	
	stage = fields.Selection([
		('draft', 'Draft'),
		('sent', 'Sent'),
		('complete', 'Complete'),
		],default = 'draft') 

	picking_type_id = fields.Many2one('stock.picking.type',string="Sending Picking Type")
	scrap_move = fields.Many2one('stock.picking.type',string="Scrap Move")
	yarn_move = fields.Many2one('stock.picking.type',string="Yarn Sending")
	fabric_move = fields.Many2one('stock.picking.type',string="Fabric Receive")

	@api.multi 
	def unlink(self): 
		for x in self: 
			if x.stage == "sent" or x.stage == "complete" : 
				raise ValidationError('Cannot Delete Record') 
		return super(FabricKnitting,self).unlink()

	@api.one
	def _load_list(self):
		self.recharge_count = self.env['knit.wizard.class'].search_count([('tree_id','=',self.id)])

	@api.multi
	def knit_receiving(self):
		return {
			'type': 'ir.actions.act_window',
			'name': 'Knitting Receiving',
			'res_model': 'knit.wizard.class',
			'view_type': 'form',
			'view_mode': 'form',
			'context': {'default_get_list': True,'readonly_by_pass': True},
		}

	@api.multi
	def in_draft(self):
		self.stage = "draft"

	@api.multi
	def in_sent(self):
		self.stage = "sent"

		inventory = self.env['stock.picking']
		inventory_lines = self.env['stock.move'].search([])
		create_inventory = inventory.create({
			'partner_id':self.name.id,
			'location_id': self.picking_type_id.default_location_src_id.id,
			'picking_type_id' : self.picking_type_id.id,
			'location_dest_id' : self.picking_type_id.default_location_dest_id.id,
			'origin': 'Fabric Knitting Dyeing',
		})

		for x in self.tree_link:
			create_inventory_lines = inventory_lines.create({
				'product_id': x.fabric.id,
				'product_uom_qty': x.required,
				'product_uom': x.fabric.uom_id.id,
				'location_id': self.picking_type_id.default_location_src_id.id,
				'picking_id': create_inventory.id,
				'name':"test",
				'location_dest_id': self.picking_type_id.default_location_dest_id.id,
				})

		self.delivery = create_inventory.id

		create_inventory.action_assign()
		create_inventory.force_assign()

		stock = self.env['stock.picking'].search([('id','=',create_inventory.id)])

		for x in stock.pack_operation_product_ids:
			x.qty_done = x.product_qty

		create_inventory.do_new_transfer()

	@api.onchange('won','name')
	def picking_type(self):
		setting = self.env['inventory.config'].search([])
		self.scrap_move = setting.knitting_dying_config_scrap.id
		self.yarn_move = setting.knitting_dying_config_yarn.id
		self.fabric_move = setting.knitting_dying_config_fabric.id
		# self.picking_type_id = setting.knitting_dying_config.id

	@api.onchange('won')
	def get_buyer(self):
		buyers = []
		styles = []
		for x in self.won:
			work_order = self.env['mrp.production'].search([('id','=',x.id)])

			if work_order.delivery:
				self.delv_date = work_order.delivery

			if work_order.buyer:
				if work_order.buyer.id not in buyers:
					buyers.append(work_order.buyer.id)

			if work_order.style_no:
				if work_order.style_no.id not in styles:
					styles.append(work_order.style_no.id)

		self.buyer = buyers
		self.style = styles

	@api.multi
	def in_house(self):
		self.stage = "in_house"

	@api.multi
	def in_complete(self):

		yarn_inventory = self.env['stock.picking'].search([])
		yarn_lines = self.env['stock.move'].search([])

		create_yarn = yarn_inventory.create({
			'partner_id':self.name.id,
			'location_id': self.scrap_move.default_location_src_id.id,
			'picking_type_id' : self.scrap_move.id,
			'location_dest_id' : self.scrap_move.default_location_dest_id.id,
			'origin': 'Yarn Scrap Move',
		})

		for x in self.tree_link:

			if x.yarn:
				for y in x.yarn:
					if y.weight:
						yarn_move = (x.a_wastage * y.weight)/100

					create_yarn_lines = yarn_lines.create({
						'product_id':y.yarn.id,
						'product_uom_qty':yarn_move,
						'product_uom': y.yarn.uom_po_id.id,
						'location_id':self.scrap_move.default_location_src_id.id,
						'picking_id': create_yarn.id,
						'name': y.yarn.name,
						'location_dest_id': self.scrap_move.default_location_dest_id.id,
						})

		create_yarn.action_assign()
		create_yarn.force_assign()

		stock = self.env['stock.picking'].search([('id','=',create_yarn.id)])

		for x in stock.pack_operation_product_ids:
			x.qty_done = x.product_qty

		create_yarn.do_new_transfer()
		self.stage = "complete"

	@api.multi
	def in_cancel(self):
		self.stage = "cancel"

class FabricKnittingTree(models.Model):
	_name = "fabric.knitting.tree"

	won = fields.Many2one('mrp.production',string="W/O", required=True)
	fabric = fields.Many2one('product.product',string="Fabric")
	yarn = fields.Many2many('yarn.move',string="Yarn")
	lot = fields.Char(string="Lot No")
	remarks = fields.Char(string="Remarks")
	sl = fields.Many2one('purchase.sl',string="S.L")
	otm = fields.Many2one('purchase.otm',string="OTM")
	dia = fields.Many2one('purchase.dia',string="Dia")
	gauge = fields.Many2one('purchase.gauge',string="Gauge")
	ndl = fields.Many2one('purchase.ndl',string="NDL")
	required = fields.Float("Required (KG)")
	receivable = fields.Float("Receivable (KG)")
	received = fields.Float("Received (KG)")
	balance = fields.Float("Balance",compute='_blc')
	wastage = fields.Char("Wastage %",compute='_wastage')
	rate  = fields.Char("Rates")
	a_wastage  = fields.Integer("Agreed Wastage")
	fabric_tree = fields.Many2one('fabric.knitting')

	@api.one
	@api.depends('receivable','received')
	def _blc(self):
		blc = self.received - self.receivable
		if blc < 0:
			self.balance = blc
		if blc > 0:
			self.balance = "+" + str(blc)

	@api.one
	@api.depends('required','balance')
	def _wastage(self):
		if self.required:
			if self.balance:
				waste = ((self.balance / self.required)* 100)
				if waste < 0:
					self.wastage = str("{0:.2f}".format(waste * (-1))) + "%"
				if waste > 0:
					self.wastage = str("{0:.2f}".format(waste)) + "%"

	@api.onchange('required','a_wastage')
	def get_reciveable(self):
		if self.required > 0.0:
			self.receivable = self.required - ((self.a_wastage * self.required)/ 100)

	@api.onchange('received')
	def get_recived(self):
		recived = self.received
		reciveable = self.receivable + (self.received*0.1)
		if recived > reciveable:
			self.recived = self.reciveable
			return {'value':{}, 'warning':{
			'title': 'Warning', 'message': 'Recived Quantity should not be greater than the Reciveable Quantity'}}

	@api.onchange('yarn')
	def get_weight(self):
		self.required = 0
		if self.yarn:
			for x in self.yarn:
				self.required = self.required + x.weight

class Knit_Receiving_Wizard(models.Model):
	_name = "knit.wizard.class"
	_rec_name = 'id'

	knit_link = fields.One2many("knit.wizard.tree","knit_tree")
	get_list = fields.Boolean("Get List")
	l_list = fields.Boolean("L List")
	tree_id = fields.Integer("ID")
	date = fields.Date("Date" ,required=True)
	name = fields.Many2one('res.partner',string = "Name")

	picking_type_id = fields.Many2one('stock.picking.type',string="Yarn Receive")
	fabric_type_id = fields.Many2one('stock.picking.type',string="Fabric Receive")
	
	stage = fields.Selection([
		('draft', 'Draft'),
		('validate', 'Validate'),
		],default="draft")

	@api.onchange('get_list')
	def get_lines(self):
 
		active_class = self.env['fabric.knitting'].browse(self._context.get('active_id'))
		data = []
		t = 0.0
		if self.get_list == True:
			self.tree_id = active_class.id
			self.name = active_class.name
			for x in active_class.tree_link:
				
				if x.receivable > 0:
					t = x.receivable - x.received
				else:
					t = x.receivable

				data.append({
					'fr_won':x.won,
					'fr_lot':x.lot,
					'fr_todo':t,
					'product': x.fabric.id,
					'yarn': x.yarn,
					'required': x.required
					})
			self.knit_link = data
			self.picking_type_id = active_class.yarn_move.id
			self.fabric_type_id = active_class.fabric_move.id

	@api.multi
	def update(self):
		active_class = self.env['fabric.knitting'].browse(self._context.get('active_id'))
		if active_class:
			self.tree_id = active_class.id
			for x in self.knit_link:
				if x.fr_done > 0:
					for y in active_class.tree_link:
						if x.fr_won == y.won:
							y.lot = x.fr_lot
							y.received = x.fr_done + y.received
							self.l_list = 'True'

		inventory = self.env['stock.picking'].search([])
		inventory_lines = self.env['stock.move'].search([])

		create_inventory = inventory.create({
			'partner_id':self.name.id,
			'location_id': self.fabric_type_id.default_location_src_id.id,
			'picking_type_id' : self.fabric_type_id.id,
			'location_dest_id' : self.fabric_type_id.default_location_dest_id.id,
			'origin': 'Fabric Knitting Reciving',
		})

		for x in self.knit_link:

			create_inventory_lines = inventory_lines.create({
				'product_id':x.product.id,
				'product_uom_qty':x.fr_done,
				'product_uom': x.product.uom_id.id,
				'location_id':self.fabric_type_id.default_location_src_id.id,
				'picking_id': create_inventory.id,
				'name': x.product.name,
				'location_dest_id': self.fabric_type_id.default_location_dest_id.id,
				})

		self.delivery = create_inventory.id

		create_inventory.action_assign()
		create_inventory.force_assign()

		stock = self.env['stock.picking'].search([('id','=',create_inventory.id)])

		for x in stock.pack_operation_product_ids:
			x.qty_done = x.product_qty

		create_inventory.do_new_transfer()

		# Creating yarn receiving

		yarn_inventory = self.env['stock.picking'].search([])
		yarn_lines = self.env['stock.move'].search([])

		create_yarn = yarn_inventory.create({
			'partner_id':self.name.id,
			'location_id': self.picking_type_id.default_location_src_id.id,
			'picking_type_id' : self.picking_type_id.id,
			'location_dest_id' : self.picking_type_id.default_location_dest_id.id,
			'origin': 'Yarn Reciving on Fabric Knitting',
		})

		for x in self.knit_link:

			if x.yarn:
				percent_count = (x.fr_done * 100)/x.required
				for y in x.yarn:
					if y.weight:
						yarn_move = (percent_count * y.weight)/100

					create_yarn_lines = yarn_lines.create({
						'product_id':y.yarn.id,
						'product_uom_qty':yarn_move,
						'product_uom': y.yarn.uom_po_id.id,
						'location_id':self.picking_type_id.default_location_src_id.id,
						'picking_id': create_yarn.id,
						'name': y.yarn.name,
						'location_dest_id': self.picking_type_id.default_location_dest_id.id,
						})

		create_yarn.action_assign()
		create_yarn.force_assign()

		stock = self.env['stock.picking'].search([('id','=',create_yarn.id)])

		for x in stock.pack_operation_product_ids:
			x.qty_done = x.product_qty

		create_yarn.do_new_transfer()

		self.stage = "validate"

class Knit_Receiving_Wizard_Tree(models.Model):
	_name="knit.wizard.tree"

	fr_won = fields.Many2one('mrp.production',string="W/O",required = True)
	yarn = fields.Many2many('yarn.move',string="Yarn")
	required = fields.Float("Required (KG)")
	fr_lot = fields.Char(string="Lot No")
	fr_todo = fields.Float(string="To Do")
	fr_done = fields.Float(string="Done")
	knit_tree = fields.Many2one("knit.wizard.class")
	product = fields.Many2one('product.product',string="Product")

	@api.onchange('fr_done')
	def get_fab_done(self):
		recived = self.fr_done
		reciveable = self.fr_todo + (self.fr_todo*0.1)

		if recived > reciveable:
			self.fr_done = self.fr_todo
			return {'value':{}, 'warning':{
			'title': 'Warning', 'message': 'Recived Quantity should not be greater than the Reciveable Quantity'}}

class ResPartnerExt(models.Model):
	_inherit = "res.partner"
	_rec_name = 'ttype'

	knitting = fields.Boolean("Knitting")
	buyer = fields.Boolean("Buyer")
	broker = fields.Boolean("Broker")
	mill = fields.Boolean("Mill")
	ttype = fields.Selection([('dye', 'Dyeing'),
		('knit', 'Knitting')
		],string = "Type") 

class ProductExt(models.Model):
	_inherit = 'product.template'

	ttype = fields.Selection([
		('yarn', 'Yarn'),
		('fabric', 'Fabric'),
		('accessories', 'Accessories'),
		('general', 'General Products'),
		('thread', 'Thread'),
		('finished', 'Fininshed Products')
		],default='yarn', required=True, string="Type")

	type = fields.Selection([
		('consu', 'Consumable'),
		('service', 'Service'),
		('product', 'Stockalble Product'),
		],default='product', required=True, string="Type")

	@api.onchange('ttype')
	def get_sales_ok(self):
		if self.ttype == 'finished':
			self.sale_ok = True
		else:
			self.sale_ok = False

class ProductVariantsExt(models.Model):
	_inherit = 'product.product'

	ttype = fields.Selection([
		('yarn', 'Yarn'),
		('fabric', 'Fabric'),
		('accessories', 'Accessories'),
		('general', 'General Products'),
		('thread', 'Thread'),
		('finished', 'Fininshed Products')
		],default='yarn', required=True, string="Type")

	accessories_type = fields.Selection([
		('wo', 'WO'),
		('thread', 'Thread'),
		('bag', 'Poly Bag'),
		('part', 'Parts')
		],default='wo', string="Accessories Type")

	net_weight = fields.Float("Net Weight")
	yarn = fields.Many2many('product.template',string="Yarn")

class PurchaseDia(models.Model):
	_name = 'purchase.dia'

	name = fields.Char("Dia",required = True)

class PurchaseSL(models.Model):
	_name = 'purchase.sl'

	name = fields.Char("SL",required = True)

class PurchaseGauge(models.Model):
	_name = 'purchase.gauge'

	name = fields.Char("Gauge",required = True)

class PurchaseNDL(models.Model):
	_name = 'purchase.ndl'

	name = fields.Char("NDL",required = True)

class PurchaseWidth(models.Model):
	_name = 'purchase.width'

	name = fields.Char("Width",required = True)

class PurchaseGSM(models.Model):
	_name = 'purchase.gsm'

	name = fields.Char("GSM",required = True)

class PurchaseProcess(models.Model):
	_name = 'purchase.process'

	name = fields.Char("Process",required = True)

class PurchaseOTM(models.Model):
	_name = 'purchase.otm'

	name = fields.Char("OTM",required = True)

class PurchasePrimary(models.Model):
	_name = 'purchase.primary'

	name = fields.Char("Primary",required = True)

class PurchaseSecondary(models.Model):
	_name = 'purchase.secondary'

	name = fields.Char("Secondary",required = True)

class PurchaseSubject(models.Model):
	_name = 'purchase.subject'

	name = fields.Char("Subject",required = True)

class PurchaseColor(models.Model):
	_name = 'purchase.color'

	name = fields.Char("Color",required = True)

class PurchaseBrnd(models.Model):
	_name = 'purchase.brand'

	name = fields.Char("Yarn Brand",required = True)

class PurchaseProdcutType(models.Model):
	_name = 'purchase.product.type'

	name = fields.Char("Product Type",required = True)

class PurchaseLot(models.Model):
	_name = 'purchase.lot'

	name = fields.Char("Lot",required = True)

class ProductType(models.Model):
	_name = 'product.type'

	name = fields.Char(string="Type",required = True)

class PurchaseProductionUnit(models.Model):
	_name = 'purchase.production.unit'

	name = fields.Char("Production Units",required = True)

class AccessoriesIssuance(models.Model):
	_name = 'purchase.access.issue'

	name = fields.Date("Date", required=True)
	wo = fields.Many2one('mrp.production',string="WO")
	unit = fields.Many2one('purchase.production.unit',string="Production Units")
	issue_Person = fields.Many2one('hr.employee', string="Issued Person")
	tree_link =fields.One2many('purchase.access.tree','access_tree')
	
	accessories_stages = fields.Selection([
		('draft', 'Open'),
		('done', 'Done'),
		],default='draft')

	picking_type_id = fields.Many2one('stock.picking.type',string="Picking Type")

	@api.multi 
	def unlink(self): 
		for x in self: 
			if x.accessories_stages == "done": 
				raise ValidationError('Cannot Delete Record') 
		return super(AccessoriesIssuance,self).unlink()

	@api.onchange('name','wo','unit','issue_Person','tree_line')
	def paicking_type(self):
		configuration = self.env['inventory.config'].search([])
		self.picking_type_id = configuration.access_issue_config.id

	@api.multi
	def in_validate(self):
		negative_vals = []
		positive_vals = []

		for x in self.tree_link:
			if x.qty > 0:
				positive_vals.append(x)
			if x.qty < 0:
				negative_vals.append(x)
		
		inventory = self.env['stock.picking']
		inventory_lines = self.env['stock.move'].search([])
		create_inventory = inventory.create({
			'picking_type_id': self.picking_type_id.warehouse_id.id,
			'location_id': self.picking_type_id.default_location_src_id.id,
			'location_dest_id': self.picking_type_id.default_location_dest_id.id,
			'origin': 'Accessories Issuance',
		})

		for x in positive_vals:
			create_inventory_lines = inventory_lines.create({
				'product_id': x.product_id.id,
				'product_uom_qty': x.qty,
				'product_uom': x.product_id.uom_id.id,
				'location_id': self.picking_type_id.default_location_src_id.id,
				'picking_id': create_inventory.id,
				'name': "Accessories Issuance",
				'location_dest_id': self.picking_type_id.default_location_dest_id.id,
			})

		for x in negative_vals:
			create_inventory_lines = inventory_lines.create({
				'product_id': x.product_id.id,
				'product_uom_qty': (-1*(x.qty)),
				'product_uom': x.product_id.uom_id.id,
				'location_id': self.picking_type_id.default_location_dest_id.id,
				'picking_id': create_inventory.id,
				'name': "Accessories Issuance",
				'location_dest_id': self.picking_type_id.default_location_src_id.id,
			})

		self.delivery = create_inventory.id

		create_inventory.action_assign()
		create_inventory.force_assign()

		stock = self.env['stock.picking'].search([('id','=',create_inventory.id)])

		for x in stock.pack_operation_product_ids:
			x.qty_done = x.product_qty

		create_inventory.do_new_transfer()

		self.accessories_stages = "done"

class AccessoriesIssuanceTree(models.Model):
	_name = 'purchase.access.tree'

	product_id = fields.Many2one('product.product',string="Product",required=True)
	uom = fields.Many2one('product.uom',string="UOM")
	qty = fields.Float("Qty Issue")
	qoh = fields.Float("Qty On hand")
	remark = fields.Char("Remarks")

	access_tree = fields.Many2one('purchase.access.issue')

	@api.onchange('product_id')
	def get_uom(self):
		if self.product_id:
			self.qoh = self.product_id.qty_available
			self.uom = self.product_id.uom_id

class HrEmployeeForm(models.Model):
	_inherit = "hr.employee"

	merchant = fields.Boolean(string="Merchant")

class InventoryConfiguration(models.Model):
	_name = "inventory.config"
	_rec_name = "name"

	name = fields.Char(string='Name',default='Settings')
	
	access_order_config = fields.Many2one('stock.picking.type',string="Sending/Receiving")
	access_issue_config = fields.Many2one('stock.picking.type',string="Sending/Receiving")

	yarn_po_config = fields.Many2one('stock.picking.type',string="Sending/Receiving")
	
	yarn_dying_config = fields.Many2one('stock.picking.type',string="Sending/Receiving")
	yarn_dying_config_scrap = fields.Many2one('stock.picking.type',string="Scrap")
	
	fabric_dying_config = fields.Many2one('stock.picking.type',string="Sending/Receiving")
	fabric_dying_config_scrap = fields.Many2one('stock.picking.type',string="Scrap")
	
	knitting_dying_config = fields.Many2one('stock.picking.type',string="Sending")
	knitting_dying_config_yarn = fields.Many2one('stock.picking.type',string="Yarn Receive")
	knitting_dying_config_fabric = fields.Many2one('stock.picking.type',string="Fabric Receive")
	knitting_dying_config_scrap = fields.Many2one('stock.picking.type',string="Scrap")

class YarnMoveClass(models.Model):
	_name = "yarn.move"
	_rec_name = "yarn"

	yarn = fields.Many2one('product.product',string="Yarn")
	weight = fields.Float(string="Quantity(Kgs)")
	