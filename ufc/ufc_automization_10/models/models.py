from openerp import models, fields, api


class ufc_automization(models.Model):
	_name = 'ufc.auto'
	_rec_name = 'name'

	name                        = fields.Char(compute = '_computed_field')
	challan_no                  = fields.Char()
	bilty_no                    = fields.Char()
	no_of_bags                  = fields.Char(string = "No of Bags")
	product                     = fields.Char(string = "Product")
	branch                      = fields.Many2one('branch',string = "Branch")
	route                       = fields.Many2one('route.management')
	orient                      = fields.Boolean(string="Orient")
	dharki                      = fields.Boolean(string="Dharki")
	engro                       = fields.Boolean(string="Engro")
	gotmachi                    = fields.Boolean(string="Machi")
	Bill_No                     = fields.Char()
	bl_number                   = fields.Many2one("bill.num",string="B/L Number")
	distance                    = fields.Float()
	party_name                  = fields.Char(string = "Party Name")
	types                       = fields.Selection([('war','Warehouse'),('sal','Salepoint')],string="Type")
	via                         = fields.Selection([('kot','Via Kot Sabzal (40KMs)'),('kash','Via Kashmore (70KMs)')],string="Via")
	additional_freight          = fields.Float(string="Additional Freight")
	additional_freight_val      = fields.Float(string="Additional Freight Value")
	region                      = fields.Many2one('regions',string = "Region")
	shipper_invoice_no          = fields.Char()
	code                        = fields.Char(string="Code")
	province                    = fields.Char(string="Province")
	dest_name                   = fields.Char(string="Destination")
	reg_code                    = fields.Char(string="Area Code")
	plan                        = fields.Char('Plan No')
	plan_date                   = fields.Char('Plan Date')
	weight                      = fields.Float()
	relevant_purchase_invoice   = fields.Many2one('ufc.auto',string="Relevant Purchase Invoice")
	sale_price                  = fields.Float(string="Company Price")
	purchase_price              = fields.Float('Total Freight')
	pun_amount                  = fields.Float('Punjab Amount')
	sin_amount                  = fields.Float('Sindh Amount')
	pun_dist                    = fields.Float('Punjab Distance')
	sin_dist                    = fields.Float('Sindh Distance')
	tax2percent                 = fields.Float('Tax @ 2%')
	profit                      = fields.Float()
	crt_no                      = fields.Char(string="Container No")
	quantity                    = fields.Char(string="Qunatity")
	misc_charges                = fields.Float(string="Misc Charges")
	supplier                    = fields.Many2one('res.partner')
	expected_company_price      = fields.Float(string = 'Expected Price')
	expected_profit             = fields.Float(string='Expected Profit')
	ean13                       = fields.Float()
	fc_paid_amount              = fields.Float(string='Paid Amount')
	remaining                   = fields.Float(string='Remaining')
	driver_photo                = fields.Binary('Driver Photo')
	billty_photo                = fields.Binary('Bilty Photo')
	payment_photo               = fields.Binary('Payment Photo')
	truck_no                    = fields.Char(string = "Truck No",required=True)
	driver_name                 = fields.Char(string = "Drive Name")
	mobile_no                   = fields.Char(string = "Mobile No")
	cleander_name               = fields.Char(string = "Cleander Name")
	cnic                        = fields.Char(string = "CNIC")
	licence_no                  = fields.Char(string = "Licence No")
	driver_payment_id           = fields.One2many('driver.payments','driver_payment')
	customer                    = fields.Many2one('res.partner',string = "Customer",required=True) 
	sequence                    = fields.Many2one('ir.sequence',string = "Sequence") 
	fiscal_position             = fields.Many2one('account.fiscal.position',string = "Fiscal Position") 
	invoice_date                = fields.Date(string = "Invoice Date",required=True) 
	journal                     = fields.Many2one('account.journal',string = "Journal") 
	account                     = fields.Many2one('account.account',string = "Account")
	order_no                    = fields.Char(index=True, readonly=True)
	state                       = fields.Selection([
								('draft', 'Draft'),
								('plan', 'Plan'),
								('bilty', 'Bilty'),
								('done', 'Done'),
								('paid', 'Paid'),
								('cancel', 'Cancel'),
								],default='draft')


	@api.multi
	def plane(self):
		self.state = 'plan'


	@api.multi
	def bilty(self):
		self.state = 'bilty'


	@api.multi
	def done(self):
		self.state = 'done'


	@api.multi
	def cancel(self):
		self.state = 'cancel'




	# ===========================giving rec_name with computed_field=======================
	# ===========================giving rec_name with computed_field=======================


	@api.depends('customer')
	def _computed_field(self):
		if self.customer:
			self.name = "Invoice of "+str(self.customer.name)


	# ===========================getting branch of active user==============================
	# ===========================getting branch of active user==============================


	@api.onchange('customer')
	def get_branch(self):
		users = self.env['res.users'].search([('id','=',self._uid)])
		if self.customer:
			self.branch = users.Branch.id


	# ========================hiding fields according to users with Boolean=================
	# ========================hiding fields according to users with Boolean=================


	@api.onchange('customer')
	def get_dharki(self):
		if self.customer.name == "Engro Fertilizer Dharki":
			self.dharki = True
			self.engro = False
			self.gotmachi = False
		if self.customer.name == "Engro Port Karachi":
			self.engro = True
			self.gotmachi = False
			self.dharki = False
		if self.customer.name == "FFC Goth Machi":
			self.gotmachi = True
			self.dharki = False
			self.engro = False
		if self.customer.name == "FFC Mir Pur Mathelo":
			self.gotmachi = True
			self.dharki = False
			self.engro = False


	# ===========calculating distance of sindh and punjab for User Engro Karachi============
	# ===========calculating distance of sindh and punjab for User Engro Karachi============


	@api.onchange('distance','sale_price')
	def dist_calculation(self):
		if self.customer.name == "Engro Port Karachi":
			per_km = self.sale_price/self.distance
			if self.region.province == "pun" and self.distance > 625:
				self.sin_dist = 625
				self.pun_dist = self.distance - self.sin_dist
				self.pun_amount = self.pun_dist * per_km
				self.sin_amount = self.sin_dist * per_km
			if self.region.province == "sin":
				self.sin_dist = self.distance
				self.sin_amount = self.sin_dist * per_km


	# ===========calculating additional freight for user Engro Dharki====================
	# ===========calculating additional freight for user Engro Dharki====================


	@api.onchange('additional_freight')
	def add_freight(self):
		if self.customer.name == "Engro Fertilizer Dharki":
			self.additional_freight_val = self.weight * self.additional_freight


	# ===========getting region code and province to display in preinvoice form ===========
	# ===========getting region code and province to display in preinvoice form ===========


	@api.onchange('region')
	def add_code(self):
		if self.region:
			self.reg_code = self.region.code
			self.province = self.region.province


	# ===========getting route code and destination to display in preinvoice form ===========
	# ===========getting route code and destination to display in preinvoice form ===========


	@api.onchange('route')
	def add_area(self):
		if self.route:
			self.code      = self.route.to.code
			self.dest_name = self.route.to.destname


	# ================================calculating tax and profit=============================
	# ================================calculating tax and profit=============================


	@api.onchange('purchase_price')
	def tax_cal(self):
		self.tax2percent = self.sale_price * .02
		self.profit      = self.sale_price - self.purchase_price - self.tax2percent


	# ============================calculating remaining and total paid=========================
	# ============================calculating remaining and total paid=========================

	@api.onchange('route','driver_payment_id','purchase_price')
	def _onchange_route(self):
		self.distance = self.route.distance
		total_paid = 0
		for x in self.driver_payment_id:
			total_paid = total_paid + x.amount
		self.fc_paid_amount = total_paid
		self.remaining = self.purchase_price - self.fc_paid_amount


	@api.onchange('remaining')
	def _onchange_stage(self):
		if self.customer:
			if self.remaining == 0.00:
				self.state = 'paid'



	@api.multi
	def create_supplier_invoice(self):
		rates_table1 = self.env['rates'].search([('company_name.id','=',self.customer.id),('date_from', '<=', self.invoice_date), ('date_to', '>=', self.invoice_date)])
		for x in rates_table1.rates_table:
			if x.distance_from  <= self.distance <= x.distance_to:
				if self.region.zone == "north":
					if x.fixed == True:
						self.expected_company_price = x.north_zone
					else:
						self.expected_company_price = self.distance * x.north_zone

				elif self.region.zone == "center":
					if x.fixed == True:
						self.expected_company_price = x.center_zone
					else:
						self.expected_company_price = self.distance * x.center_zone
				elif self.region.zone == "south":
					if x.fixed == True:
						self.expected_company_price = x.south_zone
					else:
						self.expected_company_price = self.distance * x.south_zone
				elif self.region.zone == "quetta":
					if x.fixed == True:
						self.expected_company_price = x.quetta_zone
					else:
						self.expected_company_price = self.distance * x.quetta_zone
				else:
					self.distance = 0
		self.expected_profit = self.expected_company_price - self.purchase_price


	@api.multi
	def in_progress(self):
		return self.write({'state' : 'progress'})


	# ======================creating supplier lines in cash register on create button==========
	# ======================creating supplier lines in cash register on create button==========

	@api.model
	def create(self, vals):
		vals['order_no'] = self.env['ir.sequence'].next_by_code('ufc.auto.seq')
		new_record = super(ufc_automization, self).create(vals)
		
		cash_enteries = self.env['account.bank.statement'].search([('branch.name','=',new_record.branch.name),('state','=','open')])
		if cash_enteries:
			inv = []
			for invo in new_record.driver_payment_id:
				inv.append({
					'date':invo.date,
					'name':"payment",
					'partner_id':new_record.customer.id,
					'ref':new_record.order_no,
					'amount':invo.amount*(-1),
					'line_ids':cash_enteries.id,
					})
			
			cash_enteries.line_ids = inv
			inv=[]

		return new_record

	# ===================unlinking previous lines and creating edited lines on write fun======
	# ===================unlinking previous lines and creating edited lines on write fun======


	@api.multi
	def write(self, vals):
		super(ufc_automization, self).write(vals)

		cash_enteries = self.env['account.bank.statement'].search([('branch.name','=',self.branch.name),('state','=','open')])
		if cash_enteries:
			for x in cash_enteries.line_ids:
				if x.ref == self.order_no:
					x.unlink()

			lisst= []

			for invo in self.driver_payment_id:
				lisst.append({
					'date':invo.date,
					'name':"payment",
					'partner_id':self.customer.id,
					'ref':self.order_no,
					'amount':invo.amount*(-1),
					'line_ids':cash_enteries.id,
					})
			
			cash_enteries.line_ids = lisst

		return True

	
	# ===================creating models and tree views required for preinvoice==============
	# ===================creating models and tree views required for preinvoice==============
	# ===================creating models and tree views required for preinvoice==============


class driver_payments(models.Model):
	_name       = 'driver.payments'
	# _rec_name   = 'company_name'

	name    = fields.Char(required= True, string = "Name Receiving")
	description   = fields.Char()
	cnic    = fields.Char(string = "CNIC")
	date = fields.Date(required= True)
	amount = fields.Float(required= True)

	driver_payment = fields.Many2one('ufc.auto')



class destinations(models.Model):
	_name = 'destinations'

	_rec_name = 'destname'

	destname = fields.Char(string="Name")
	code = fields.Char(string="Code")


class route_management(models.Model):
	_name = 'route.management'
	name = fields.Char('Name')
	route_description = fields.Text('Description')
	xx_from           = fields.Many2one('destinations',string = "From")
	to                = fields.Many2one('destinations',string = "To")
	distance          = fields.Float()

	_sql_constraints = [
	('name_unique', 'unique(name)', 'This Route already exists!')
	]


	@api.onchange('xx_from','to')
	def route_defination_name_get(self):
		if self.xx_from.destname and self.to.destname:
			self.name = self.xx_from.destname +' to '+ self.to.destname
		else:
			return


class bill(models.Model):
	_name = 'bill.num'

	name = fields.Char(string="B/L Number")



class regions(models.Model):
	_name = 'regions'


	name = fields.Char()
	code = fields.Char()
	province = fields.Selection([
		('pun','Punjab'),
		('sin','Sindh'),
		('bal','Balochistan'),
		('kpk','KPK'),
		('gbl','Gilgit Baltistan')
		],string="Province")
	zone = fields.Selection([
		('north','North Zone'),
		('south','South Zone'),
		('center','Center Zone'),
		('queeta','Queeta Zone'),
		],string="Zone")


	
class rates_table(models.Model):
	_name       = 'rates.table'

	distance_from      = fields.Float()
	distance_to        = fields.Float()
	north_zone         = fields.Float()
	center_zone        = fields.Float()
	south_zone         = fields.Float()
	quetta_zone        = fields.Float()
	fixed              = fields.Boolean()

	rates_table_id = fields.Many2one('rates')




class rates(models.Model):
	_name       = 'rates'
	_rec_name   = 'company_name'

	date_from    = fields.Date(required=True, string='Date From')
	date_to    = fields.Date(required=True,string='Date From')
	company_name = fields.Many2one('res.partner',string = 'Company Name',required=True)

	rates_table = fields.One2many('rates.table', 'rates_table_id')

