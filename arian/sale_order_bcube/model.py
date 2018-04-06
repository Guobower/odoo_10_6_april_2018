# -*- coding: utf-8 -*- 
from odoo import models, fields, api


class sale_order_extension(models.Model): 
	_inherit = 'sale.order'

	internal_order_num = fields.Char(string="Internal Order No")
	lc_no = fields.Char(string="LC Number")
	customer_purchase_no = fields.Char(string="Customer Purchase No")
	pin = fields.Char(string="PIN #")
	partial_shipment = fields.Char(string="Partial Shipment")
	transhipment = fields.Char(string="Transhipment")
	lot = fields.Char(string="Lot")
	qty_ctn = fields.Char(string="Qty/CTN")
	loading_port = fields.Char(string="Port of Loading")

	delivery_date = fields.Date(string="Delivery Date")
	p_date = fields.Date(string="P. invoicing Date")
	etd_khi = fields.Date(string="ETD KHI")

	carrier_id = fields.Many2one("delivery.carrier", string="Trade terms")
	inco_terms = fields.Many2one('stock.incoterms',string="Inco Terms")
	invoice_bank = fields.Many2one('res.bank',string="Bank")
	currency = fields.Many2one('res.currency',string="Currency")

	# 19/07/2017 awais
	bl_no=fields.Integer("BL Number")
	bl_date=fields.Date("BL Date")
	e_form=fields.Integer("E FORM No")
	t_carton=fields.Integer("Total Cartons")

	# 19/07/2017 awais

	
	payment_type = fields.Selection([
		('payable','Payable'),
		('nonpayable','Non-Payable')
		],default='payable',string="Payment Type")

	ship_via = fields.Selection([
		('bysea', 'By Sea'),
		('byair', 'By Air'),
		('byland', 'By Land'),
		],default='bysea', string="Ship via")
	
	invoicing_address = fields.Text(string="Invoice Address")
	shiping_address = fields.Text(string="Shiping Address")


	# @api.onchange('partner_id')
	# def onchange_partner_id(self):
	# 	rec = self.env['res.partner'].search([('name','=',self.partner_id.name)])
	# 	self.inco_terms = rec.incoterms.id
	
	@api.multi
	def generate_wizard(self):
		return {
		'type': 'ir.actions.act_window',
		'name': 'Add Products',
		'res_model': 'wizard.class',
		'view_type': 'form',
		'view_mode': 'form',
		'target' : 'new',
		# 'context': {'partner_id': self.partner_id.id,
		# 			'sale_order_no':self.id},
		}


class stock_picking_own(models.Model):
	_inherit 	= 'stock.picking'


	def do_new_transfer(self):
		new_record = super(stock_picking_own, self).do_new_transfer()

		sale_order = self.env['sale.order'].search([('name','=',self.origin)])
		purchase_order = self.env['purchase.order'].search([('name','=',self.origin)])

		invoice = self.env['account.invoice'].search([])
		invoice_lines = self.env['account.invoice.line'].search([])

		if sale_order:
			create_invoice = invoice.create({
				'partner_id':sale_order.partner_id.id,
				'confirmation_date':sale_order.confirmation_date,
				'delivery_date':sale_order.delivery_date,
				'Lc_no' : sale_order.lc_no,
				'customer_order_no' : sale_order.customer_purchase_no,
				'payment_term_id' : sale_order.payment_term_id.id,
				'journal_id': 1,
				'invoice_bank':sale_order.invoice_bank.id,
				'qty_ctn':sale_order.qty_ctn,
				'lot':sale_order.lot,
				'pin':sale_order.pin,
				'partial_shipment':sale_order.partial_shipment,
				'LC_no':sale_order.lc_no,
				'inco_terms':sale_order.inco_terms.id,
				'invoice_address':sale_order.invoicing_address,
				'bl_no':sale_order.bl_no,
				'e_form_no':sale_order.e_form,
				'etd_khi':sale_order.etd_khi,
				'ship_mode':sale_order.ship_via,
				'loading_port':sale_order.loading_port,
				'ship_to_address':sale_order.shiping_address,
				'bl_date':sale_order.bl_date,
				'transhipment':sale_order.transhipment,
				'performa':sale_order.name,
				'sale_order_num': sale_order.id
				
				})

			for x in sale_order.order_line:
				for y in self.pack_operation_product_ids:
					if x.product_id.id == y.product_id.id:
						if y.qty_done > 0:

							if x.product_id.property_account_income_id.id:
								account_id = x.product_id.property_account_income_id.id
							else:
								account_id = x.product_id.categ_id.property_account_income_categ_id.id	

							create_invoice_lines= invoice_lines.create({
								'product_id':x.product_id.id,
								'name':x.name,
								'quantity': y.qty_done,
								'account_id': account_id,
								'invoice_id' : create_invoice.id,
								'price_unit': x.price_unit,
								})

				packing_list = self.env['commercial.packing.list'].search([])

				create_packing_list = packing_list.create({
					'invoice_no': create_invoice.id,
					})


		if purchase_order:
			create_invoice = invoice.create({
				'journal_id': 3,
				'partner_id':purchase_order.partner_id.id,
				'date_invoice' : purchase_order.date_order,
				'reference':purchase_order.partner_ref,
				'origin':purchase_order.name,
				'type':"in_invoice",
				})
			for x in purchase_order.order_line:
				for y in self.pack_operation_product_ids:
					if x.product_id.id == y.product_id.id:
						if x.product_id.property_account_income_id.id:
							account_id = x.product_id.property_account_income_id.id
						else:
							account_id = x.product_id.categ_id.property_account_income_categ_id	
						create_invoice_lines= invoice_lines.create({
							'product_id':x.product_id.id,
							'quantity': y.qty_done,
							'price_unit': x.price_unit,
							'price_subtotal': x.price_subtotal,
							'account_id': 3,
							'name' : x.name,
							'invoice_id' : create_invoice.id
							})
		return new_record

class EcubeSaleOrderLine(models.Model):
	_inherit 	= 'sale.order.line'

	size=fields.Many2one("product.attribute.value","Size")

class wizard_tree(models.Model):
  _name="wizard.tree"

  attr_val     = fields.Many2many('product.attribute.value',string="Attribute Values")
  qty  = fields.Float(string="Quantity")
  prod_name = fields.Many2one("wizard.class")
  product_product = fields.Many2one('product.product','Variant')

class wizard_class(models.Model):
	_name = "wizard.class"

	product_tree  = fields.One2many("wizard.tree","prod_name")
	product      = fields.Many2one('product.template',"Product")
	
	@api.onchange('product')
	def generate_list(self):

		products = self.env['product.template'].search([('id','=',self.product.id)])

		data = []
		for x in products.product_variant_ids:
			data.append({
				'product_product':x.id,
				'prod_name':self.id
				})
			self.product_tree = data

	@api.multi
	def generate(self):
	  active_class = self.env['sale.order'].browse(self._context.get('active_id'))
	  if active_class:
		for x in self.product_tree:
		  if x.qty >0:
			generate_so_line= active_class.order_line.create({
			  'product_id': x.product_product.id,
			  'product_uom_qty':x.qty,
			  'order_id': active_class.id
			  })