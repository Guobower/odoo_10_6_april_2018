# -*- coding: utf-8 -*- 
from odoo import models, fields, api

class Merchandising(models.Model):
	_name = 'merchandising.costing'
	_rec_name = 'won'

	won = fields.Many2one('mrp.production', string="Work Order")
	buyer = fields.Many2one('res.partner',string='Buyer', required=True)
	style = fields.Many2one('style.number',string="Style No")
	currency = fields.Many2one('res.currency',string="Currency")
	category = fields.Many2one('merchandising.category',string="Category")
	garment = fields.Many2one('product.product',string="Garment Description")

	customer_po = fields.Char(string="Customer PO#")
	style_name = fields.Char(string="Style Name")

	product_image = fields.Binary(string="Product Picture")

	currency_rate = fields.Float(string="Currency Rate")
	total_fabric = fields.Float(string="Total Cost(Rs)",compute='total_cost')
	total_access = fields.Float(string="Total Cost(Rs)",compute='access_total')
	total_service = fields.Float(string="Total Cost(Rs)",compute='service_total')
	total_pack = fields.Float(string="Total Cost(Rs)",compute='pack_total')
	total_access_pack = fields.Float(string="Total Cost(Rs)",compute='pack_access_total')
	total_others = fields.Float(string="Total Cost(Rs)",compute='others_total')
	
	fabric_dollar = fields.Monetary(compute='total_dollars',currency_field='currency')
	access_dollar = fields.Monetary(compute='access_dollars',currency_field='currency')
	service_dollar = fields.Monetary(compute='service_dollars',currency_field='currency')
	pack_dollar = fields.Monetary(compute='pack_dollars',currency_field='currency')
	access_pack_dollar = fields.Monetary(compute='access_pack_dollars',currency_field='currency')
	others_dollar = fields.Monetary(compute='others_dollars',currency_field='currency')

	fabric_tree = fields.One2many('fabric.costing','link')
	access_tree = fields.One2many('access.stich','link')
	pack_tree = fields.One2many('access.packing','link')
	service_tree = fields.One2many('service.costing','link')
	packing_tree = fields.One2many('packing.costing','link')
	others_tree = fields.One2many('others.cost','link')
	tech_tree = fields.One2many('teck.pack','link')
	consumption_tree = fields.One2many('consumption.cost','link')

	@api.onchange('won')
	def total_costing(self):
		if self.won:
			self.buyer = self.won.buyer.id
			self.style = self.won.style_no.id
			self.garment = self.won.product_id.id
			self.customer_po = self.won.custome_po

	@api.depends('fabric_tree')
	def total_cost(self):
		cost = 0
		for x in self.fabric_tree:
			cost = cost + x.total

		self.total_fabric = cost

	@api.depends('total_fabric')
	def total_dollars(self):
		if self.total_fabric and self.currency_rate:
			self.fabric_dollar = self.total_fabric/self.currency_rate

	@api.depends('access_tree')
	def access_total(self):
		cost = 0
		for x in self.access_tree:
			cost = cost + x.costing

		self.total_access = cost

	@api.depends('total_access')
	def access_dollars(self):
		if self.total_access and self.currency_rate:
			self.access_dollar = self.total_access/self.currency_rate

	@api.depends('service_tree')
	def service_total(self):
		cost = 0
		for x in self.service_tree:
			cost = cost + x.costing

		self.total_service = cost

	@api.depends('total_service')
	def service_dollars(self):
		if self.total_service and self.currency_rate:
			self.service_dollar = self.total_service/self.currency_rate

	@api.depends('packing_tree')
	def pack_total(self):
		cost = 0
		for x in self.packing_tree:
			cost = cost + x.total

		self.total_pack = cost

	@api.depends('total_pack')
	def pack_dollars(self):
		if self.total_pack and self.currency_rate:
			self.pack_dollar = self.total_pack/self.currency_rate

	@api.depends('pack_tree')
	def pack_access_total(self):
		cost = 0
		for x in self.pack_tree:
			cost = cost + x.costing

		self.total_access_pack = cost

	@api.depends('total_access_pack')
	def access_pack_dollars(self):
		if self.total_access_pack and self.currency_rate:
			self.access_pack_dollar = self.total_access_pack/self.currency_rate

	@api.depends('others_tree')
	def others_total(self):
		cost = 0
		for x in self.others_tree:
			cost = cost + x.costing

		self.total_others = cost

	@api.depends('total_others')
	def others_dollars(self):
		if self.total_others and self.currency_rate:
			self.others_dollar = self.total_others/self.currency_rate

	@api.multi
	def defaults(self):
		packings = self.env['packing.accessories'].search([('boolean','=','True')])
		stiching = self.env['stiching.accessories'].search([('boolean','=','True')])
		others = self.env['others.accessories'].search([('boolean','=','True')])
		services = self.env['others.services'].search([('boolean','=','True')])
		consumption = self.env['consumption.type'].search([('boolean','=','True')])

		packs = []
		stichs = []
		other = []
		service = []
		consump = []

		for y in self.pack_tree:
			packs.append(y.defaults.id)

		for y in self.access_tree:
			stichs.append(y.defaults.id)

		for y in self.others_tree:
			other.append(y.defaults.id)

		for y in self.service_tree:
			service.append(y.service.id)

		for y in self.consumption_tree:
			consump.append(y.typed.id)

		for x in packings:
			if x.id not in packs:
				create_reorder = self.env['access.packing'].create({
					'defaults': x.id,
					'link': self.id
				})

		for x in stiching:
			if x.id not in stichs:
				create_reorder = self.env['access.stich'].create({
					'defaults': x.id,
					'link': self.id
				})

		for x in others:
			if x.id not in other:
				create_reorder = self.env['others.cost'].create({
					'defaults': x.id,
					'link': self.id
				})

		for x in services:
			if x.id not in service:
				create_reorder = self.env['service.costing'].create({
					'service': x.id,
					'link': self.id
				})

		for x in consumption:
			if x.id not in consump:
				create_reorder = self.env['consumption.cost'].create({
					'typed': x.id,
					'link': self.id
				})

class MerchandisingFabricTree(models.Model):
	_name = 'fabric.costing'
	_rec_name = 'fabric'

	fabric = fields.Many2one('product.product', string="Fabric", required=True)
	fabricno = fields.Many2one('seperate.fabric', string="Fabric No.")
	yarn = fields.Many2many('seperate.yarn', string="Yarn")

	texture = fields.Char(string="Texture")
	contents = fields.Char(string="Contents")
	gsm = fields.Char(string="GSM")
	dia = fields.Char(string="DIA")
	guage = fields.Char(string="Guage")
	width = fields.Char(string="Width Option")
	color = fields.Char(string="Colors")
	dye_rate = fields.Char(string="Dyeing Rate")
	dye_wast = fields.Char(string="Wastage")
	knit_rate = fields.Char(string="Knitting Rate")
	knit_wast = fields.Char(string="Wastage")
	rotary_rate = fields.Char(string="Rotary Rate")
	total = fields.Float(string="Total")
	Kniting = fields.Float(string="Kniting")
	knit_wastage = fields.Float(string="Knitting Wastage %")
	wash_wastage = fields.Float(string="Washing Wastage %")
	washingdyeing = fields.Float(string="Washing/Dyeing")
	total_yarn = fields.Float(string="Total")

	link = fields.Many2one('merchandising.costing')

	@api.onchange('yarn')
	def yarn_costing(self):
		if self.yarn:
			for x in self.yarn:
				self.total = x.yarnrate + x.yarndyeing + x.Twisting

	@api.onchange('yarn','Kniting','knit_wastage','wash_wastage','washingdyeing')
	def total_costing(self):
		qty = 0
		for x in self.yarn:
			qty = qty + x.total_yarn

		knitting = self.Kniting + (self.Kniting*self.knit_wastage)/100
		washing = self.washingdyeing + (self.washingdyeing*self.wash_wastage)/100

		self.total_yarn = knitting + washing + qty

class MerchandisingAccessoriesTree(models.Model):
	_name = 'access.stich'
	_rec_name = 'access'

	access = fields.Many2one('product.product', string="Accessories")
	defaults = fields.Many2one('stiching.accessories',string="Accessories Type")
	qty = fields.Float(string="Quantity",default='1.00')
	costing = fields.Float(string="Price")
	remarks = fields.Char(string="Description")
	typed = fields.Selection([
		('local', 'Local'),
		('imported', 'Imported'),
		],default='local')

	link = fields.Many2one('merchandising.costing',string="link")

class MerchandisingAccessoriesPackingTree(models.Model):
	_name = 'access.packing'
	_rec_name = 'access'

	access = fields.Many2one('product.product', string="Accessories")
	defaults = fields.Many2one('packing.accessories', string="Accessories Type", required=True)
	qty = fields.Float(string="Quantity",default='1.00')
	costing = fields.Float(string="Price")
	remarks = fields.Char(string="Description")
	typed = fields.Selection([
		('local', 'Local'),
		('imported', 'Imported'),
		],default='local')

	link = fields.Many2one('merchandising.costing',string="link")

class MerchandisingAccessoriesPackingTree(models.Model):
	_name = 'others.cost'
	_rec_name = 'defaults'

	defaults = fields.Many2one('others.accessories', string="Other Items", required=True)
	qty = fields.Float(string="Quantity",default='1.00')
	costing = fields.Float(string="Price")
	remarks = fields.Char(string="Description")
	typed = fields.Selection([
		('local', 'Local'),
		('imported', 'Imported'),
		],default='local')

	link = fields.Many2one('merchandising.costing',string="link")

class MerchandisingServicesTree(models.Model):
	_name = 'service.costing'
	_rec_name = 'service'

	service = fields.Many2one('others.services',string="Services", required=True)
	uom = fields.Char(string="Unit of Measure")
	costing = fields.Float(string="Costing")
	remarks = fields.Char(string="Remarks")

	link = fields.Many2one('merchandising.costing',string="link")

class MerchandisingPackingTree(models.Model):
	_name = 'packing.costing'
	_rec_name = 'description'

	description = fields.Char(string="Description", required=True)
	unit_price = fields.Float(string="Unit Price")
	quantity = fields.Float(string="Quantity")
	total = fields.Float(string="Total")
	remarks = fields.Char(string="Remarks")

	link = fields.Many2one('merchandising.costing',string="link")

class MerchandisingTeckPackTree(models.Model):
	_name = 'teck.pack'
	_rec_name = 'description'

	description = fields.Char(string="Description")
	tech_pack = fields.Binary(string="Tech Pack")

	link = fields.Many2one('merchandising.costing',string="link")

class MerchandisingConsumptionTree(models.Model):
	_name = 'consumption.cost'
	_rec_name = 'typed'

	typed = fields.Many2one('consumption.type',string="Garments Description")
	uom = fields.Many2one('consumption.uom',string="Unit of Measure")
	parts = fields.Char(string="Parts")
	fac = fields.Char(string="FAC")
	gsm = fields.Char(string="GSM")
	consumption = fields.Char(string="Consumption")

	link = fields.Many2one('merchandising.costing',string="link")

	@api.onchange('uom')
	def total_fbl(self):
		if self.uom:
			self.parts = self.uom.parts
			self.fac = self.uom.fac
			self.gsm = self.uom.gsm
			self.consumption = self.uom.final_consumption

class MerchandisingYarnMove(models.Model):
	_name = "merchandising.yarn.move"
	_rec_name = "yarn"

	yarn = fields.Many2one('product.product',string="Yarn")
	weight = fields.Float(string="Quantity(Kgs)")
	cost = fields.Float(string="Cost(Kgs)")
	ratio = fields.Char(string="Ratio(Kgs)")

class MerchandisingCategory(models.Model):
	_name = "merchandising.category"
	_rec_name = "name"

	name = fields.Char(string="Name")

class DefaultAccessoriesStiching(models.Model):
	_name = "stiching.accessories"
	_rec_name = "name"

	name = fields.Char(string="Name")
	boolean = fields.Boolean(string="Is Default")

class DefaultAccessoriesPacking(models.Model):
	_name = "packing.accessories"
	_rec_name = "name"

	name = fields.Char(string="Name")
	boolean = fields.Boolean(string="Is Default")

class DefaultAccessoriesOthers(models.Model):
	_name = "others.accessories"
	_rec_name = "name"

	name = fields.Char(string="Name")
	boolean = fields.Boolean(string="Is Default")

class DefaultAccessoriesConsuption(models.Model):
	_name = "consumption.uom"
	_rec_name = "final_consumption"

	cm_fbl = fields.Float(string="FBL")
	cm_chest = fields.Float(string="Chest")
	parts = fields.Float(string="Parts")
	fac = fields.Float(string="FAC")
	gsm = fields.Float(string="GSM")
	cm_percent = fields.Char(string="Percentage %")

	inch_fbl = fields.Float(string="FBL")
	inch_chest = fields.Float(string="Chest")

	ml_fbl = fields.Float(string="FBL")
	ml_chest = fields.Float(string="Chest")
	ml_percent = fields.Float(string="Percentage %")

	partial = fields.Float(string="Partial Consumption")
	final_consumption = fields.Float(string="Final Consumption")

	@api.onchange('cm_fbl')
	def total_fbl(self):
		if self.cm_fbl:
			self.inch_fbl = self.cm_fbl/2.54
			self.ml_fbl = self.inch_fbl + 1.5

	@api.onchange('cm_chest')
	def total_chest(self):
		if self.cm_chest:
			self.inch_chest = self.cm_chest /2.54
			self.ml_chest = self.inch_chest + 1

	@api.onchange('ml_fbl','ml_chest','parts','fac','gsm')
	def total_percent(self):
		if self.ml_fbl and self.ml_chest and self.parts and self.fac and self.gsm:
			self.ml_percent = (self.ml_fbl*self.ml_chest*self.parts*self.gsm)/(self.fac)

	@api.onchange('cm_percent','ml_percent')
	def total_partial(self):
		if self.cm_percent and self.ml_percent:
			self.partial = (self.ml_percent*float(self.cm_percent)/100)

	@api.onchange('partial','ml_percent')
	def total_consumption(self):
		if self.partial and float(self.ml_percent):
			self.final_consumption = (self.partial + self.ml_percent)

class DefaultAccessoriesType(models.Model):
	_name = "consumption.type"
	_rec_name = "name"

	name = fields.Char(string="Name")
	boolean = fields.Boolean(string="Is Default")

class DefaultServises(models.Model):
	_name = "others.services"
	_rec_name = "name"

	name = fields.Char(string="Name")
	boolean = fields.Boolean(string="Is Default")

class SeprateFabricClass(models.Model):
	_name = "seperate.fabric"
	_rec_name = "name"

	name = fields.Char(string="Name")

class SeprateYarnClass(models.Model):
	_name = "seperate.yarn"
	_rec_name = "count"

	name = fields.Char(string="Yarn")
	count = fields.Many2one('product.product',string="Yarn count",required=True)
	percentage = fields.Float(string="Consumption %",required=True)
	countlbs = fields.Float(string="Rate/Lbs",digits=(19,4))
	yarnrate = fields.Float(string="Rate/KG",digits=(19,4))
	total_yarn = fields.Float(string="Total Yarn")

	yarndyeing = fields.Float(string="Yarn Dyeing")
	yarn_wastage = fields.Float(string="Yarn Wastage %")
	Twisting = fields.Float(string="Twisting")
	twist_wastage = fields.Float(string="Twisting Wastage %")
	invisible = fields.Float(string="Other")

	@api.onchange('yarnrate')
	def total_lbs(self):
		if self.yarnrate:
			self.countlbs = self.yarnrate * 2.2046

	@api.onchange('countlbs')
	def total_kgs(self):
		if self.countlbs:
			self.yarnrate = self.countlbs / 2.2046

	@api.onchange('percentage','yarndyeing','yarn_wastage','Twisting','twist_wastage','invisible')
	def yarn_total(self):
		if self.percentage:
			dying = self.yarndyeing + (self.yarndyeing*self.yarn_wastage)/100
			twisting = self.Twisting + (self.Twisting*self.twist_wastage)/100

			self.total_yarn = ((dying + twisting + self.invisible + self.yarnrate)*self.percentage)/100