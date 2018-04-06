# -*- coding: utf-8 -*- 
from odoo import models, fields, api
from openerp.exceptions import Warning, ValidationError

class product_portfolio(models.Model): 
    _name = 'product.portfolio'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    name = fields.Char(string="Name", required=True)

    quantity = fields.Integer(string="Quantity")

    order_date = fields.Date(string="Date")
    delivery_date = fields.Date(string="Delivery Date")

    customer_name = fields.Many2one('res.partner', string="Customer", required= True )
    unit_measurement = fields.Many2one('product.uom', string="Unit of Measurement")
    project = fields.Many2one('project.product', string="Project", required= True )
    product_catagory = fields.Many2one('product.category', string="Product Catagory", required= True)
    
    description = fields.Text(string="Description")
    
    stages     = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('validate', 'Validate'),
        ('cancel', 'Cancel'),
        ],default='draft')

    @api.multi
    def in_progress(self):
        self.stages = "in_progress"
        _inherit = 'product.prototype'

        similar_id = self.env['product.prototype'].search([('prototype_development_request','=',self.id)])

        if not similar_id:

            create_reorder = self.env['product.prototype'].create({
                'prod_name':self.name,
                'prototype_order_date':self.order_date,
                'deadline_date':self.delivery_date,
                'prototype_product_catagory':self.product_catagory.id,
                'prototype_customer_name':self.customer_name.id,
                'prototype_customer_name':self.customer_name.id,
                'internal_note':self.description,
                'unit_measurement_prototype':self.unit_measurement.id,
                'prototype_development_request':self.id,
                'quantity': self.quantity,
                'projects': self.project.id

            })

            for x in self.devlopment_varients:
                create_variants = self.env['prototype.attribute'].create({
                    'attribute_id': x.attribute_id.id,
                    'product_tmpl_id':x.product_tmpl_id.id ,
                    'attribute_development': create_reorder.id
                })
                line_data = self.env['prototype.attribute'].search([('id','=',create_variants.id)])
                for a in line_data:
                    for z in x.value_ids:
                        a.value_ids = [(4,z.id)]
                        
    @api.multi
    def validate(self):
        self.stages = "validate"

    @api.multi
    def cancel(self):
        self.stages = "cancel"

    devlopment_varients = fields.One2many('development.attribute','attribute_development')

class product_prototype(models.Model): 
    _name = 'product.prototype'
    _rec_name = 'prod_name'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    prod_name = fields.Char(string="Name", required= True)
    inner_carton = fields.Char(string="Inner Carton")
    pcs_carton = fields.Char(string="Pcs/Carton")

    quantity = fields.Integer(string="Quantity")

    total_cost = fields.Float(string="Total Cost", readonly= True)
    total_cost_service = fields.Float(string="Total Cost", compute='_compute_total_cost_prototype')
    total_cost_prototype = fields.Float(string="Total Cost", compute='_compute_total_cost_prototype')
    dollar_rate = fields.Float(string="Rate of Dollar", readonly= True)
    dollar_price = fields.Float(string="Dollar Price", readonly= True)
    carton_master_height = fields.Float(string="Height")
    freight = fields.Float(string="Freight")

    #------------ Packing Details ---------------#
    length = fields.Float(string="Lenght")
    width = fields.Float(string="Width")
    height = fields.Float(string="Height")
    counted_volume = fields.Float("Vloume")
    net_weight = fields.Float(string="Net Weight (Gms)")
    grossed_weight = fields.Float(string="Gross Weight (Gms)")
    size_from = fields.Float(string="Size From")
    size_to = fields.Float(string="Size to")
    inner_carton = fields.Char(string="Inner Carton")

    carton_lenght = fields.Float(string="Lenght")
    carton_height = fields.Float(string="Height")
    carton_width = fields.Float(string="Width")
    counted_volume_2 = fields.Float("Vloume")
    carton_net_weight = fields.Float(string="Net Weight (Gms)")
    carton_weight = fields.Float(string="Gross Weight (Gms)")
    pcs_carton = fields.Char(string="Pcs/Carton")
    #--------------------------------------------#

    prototype_order_date = fields.Date(string="Date")
    complition_date = fields.Date(string="Expected Complition Date")
    deadline_date = fields.Date(string="Deadline Date")
    
    prototype_customer_name = fields.Many2one('res.partner', string="Customer" )
    prototype_product_catagory = fields.Many2one('product.category', string="Product Catagory", required= True)
    prototype_development_request = fields.Many2one('product.portfolio', string="Development Request")
    prototype_bill = fields.Many2one('mrp.bom', string="Bill of Material")
    projects = fields.Many2one('project.product', string="Projects")
    unit_measurement_prototype = fields.Many2one('product.uom', string="Unit of Measurement")
    proto_product = fields.Many2one("product.template",string="Product")
    
    prototype_description = fields.Text(string="Description")
    internal_note = fields.Text(string="Description")
    
    prototype_tech_pack = fields.Binary(string="Tech Pack")
    prototype_pattern = fields.Binary(string="Pattern")
    
    prototype_stages = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('qa', 'QA'),
        ('client_testing', 'Client Testing'),
        ('approved', 'Approved'),
        ('cancel', 'Cancel'),
        ],default='draft')

    prototype_cost = fields.One2many('prototype.cost','prototype_id')
    prototype_services = fields.One2many('prototype.services','total_service')
    devlopment_varients = fields.One2many('prototype.attribute','attribute_development')

    @api.onchange('prototype_cost')
    def on_change_prod_cost(self):

        cost_total = 0
        for x in self.prototype_cost:
            cost_total = cost_total + x.cost

        self.total_cost = cost_total

        if self.dollar_rate > 0:
            self.dollar_price = self.total_cost/self.dollar_rate
        self.total_cost_prototype = self.total_cost+self.total_cost_service

    @api.one
    @api.depends('prototype_services')
    def _compute_total_cost_prototype(self):

        cost_total = 0
        for x in self.prototype_services:
            cost_total = cost_total + x.subcost

        self.total_cost_service = cost_total
        self.total_cost_prototype = self.total_cost+self.total_cost_service

    @api.multi
    def progress_in(self):
        self.prototype_stages = "in_progress"

    @api.multi
    def qa(self):
        self.prototype_stages = "qa"

    @api.multi
    def client_testing(self):
        self.prototype_stages = "client_testing"

    @api.multi
    def approved(self):
        self.prototype_stages = "approved"
        _inherit = 'product.template'

        if not self.proto_product:

            create_reorder = self.env['product.template'].create({
                'name':self.prod_name,
                'purchase_ok': False,
                'prod_customer':self.prototype_customer_name.id,
                'categ_id':self.prototype_product_catagory.id,
                'uom':self.unit_measurement_prototype.id,
                'length': self.length,
                'width': self.width,
                'height': self.height,
                'grossed_weight': self.grossed_weight,
                'size_from': self.size_from,
                'size_to': self.size_to,
                'carton_lenght': self.carton_lenght,
                'carton_width': self.carton_width,
                'carton_height': self.carton_height,
                'carton_weight': self.carton_weight,
                'carton_master_height': self.carton_master_height,
                'standard_price': self.total_cost_prototype,
                'description_purchase': self.internal_note,
                'description_sale':self.prototype_description,
            })

            for x in self.devlopment_varients:
                create_variants = self.env['product.attribute.line'].create({
                    'attribute_id': x.attribute_id.id,
                    'product_tmpl_id':create_reorder.id
                })
                line_data = self.env['product.attribute.line'].search([('id','=',create_variants.id)])
                for a in line_data:
                    for z in x.value_ids:
                        a.value_ids = [(4,z.id)]

            self.proto_product = create_reorder.id
        else:
            raise ValidationError("Product already exist named as " + self.proto_product.name)
    @api.multi
    def cancel(self):
        self.prototype_stages = "cancel"

    @api.multi
    def color(self):
        color_name = ""
        for x in self.devlopment_varients:
            if x.attribute_id.name == "color":
                for y in x.value_ids:
                    color_name = str(color_name) + y.name + " - "
        return color_name

    @api.multi
    def size(self):
        color_name = ""
        for x in self.devlopment_varients:
            if x.attribute_id.name == "size":
                for y in x.value_ids:
                    color_name = str(color_name) + y.name + " - "
        return color_name

class prototype_cost(models.Model): 
    _name = 'prototype.cost'

    rate = fields.Float(string="Rate")
    pair = fields.Float(string="Pair")
    consumption = fields.Float(string="Consumption")
    cost = fields.Float(string="Cost", readonly = True)

    remarks = fields.Char(string="Remarks")
    
    product = fields.Many2one('product.product', string="Product" )
    prod_type = fields.Many2one('product.category', string="Product Category")
    unit = fields.Many2one('product.uom', string="Unit")

    prototype_id = fields.Many2one('product.prototype')
    
    type_of_work = fields.Selection([
        ('outter_shell', 'Outer Shell'),
        ('inside', 'Inside'),
        ('accessories', 'Accessories'),
        ('makery', 'Makery'),
        ],default='outter_shell', string="Type")

    @api.onchange('product')
    def on_change_prod_name(self):
        self.rate = self.product.standard_price
        self.unit = self.product.uom_id
        self.prod_type = self.product.categ_id

    @api.onchange('rate')
    def on_change_rate(self):
        if self.pair > 0:
            self.cost = self.rate/self.pair
            
        if self.consumption > 0:
            self.cost = self.rate*self.consumption

    @api.onchange('pair')
    def on_change_pair(self):
        if self.pair != 0:
            self.consumption = 0
        
        if self.pair > 0:
            self.cost = self.rate/self.pair
            
        if self.consumption > 0:
            self.cost = self.rate*self.consumption

    @api.onchange('consumption')
    def on_change_consumption(self):
        if self.consumption != 0:
            self.pair = 0

        if self.pair > 0:
            self.cost = self.rate/self.pair
            
        if self.consumption > 0:
            self.cost = self.rate*self.consumption

class prototype_services(models.Model): 
    _name = 'prototype.services'

    service = fields.Char(string="Service")

    rate = fields.Float(string="Rate")
    subcost = fields.Float(string="Sub-Cost", compute='_compute_subcost')

    unit_measurement = fields.Many2one('product.uom', string="Unit of Measurement")
    total_service = fields.Many2one('product.prototype')

    # @api.onchange('hours')
    # def on_change_hours(self):
    #     self.subcost = self.hours*self.rate

    @api.one
    @api.depends('rate')
    def _compute_subcost(self):
        self.subcost = self.rate

class wizerd_prototype(models.Model): 
    _name = 'wizerd.prototype'

    prod_name = fields.Char(string="Name", required= True)
    
    prototype_order_date = fields.Date(string="Date")
    
    prototype_customer_name = fields.Many2one('res.partner', string="Customer" )
    prototype_product_catagory = fields.Many2one('product.category', string="Product Catagory", required= True)
    prototype_development_request = fields.Many2one('product.portfolio', string="Development Request")
    prototype_bill = fields.Many2one('mrp.bom', string="Bill of Material")
    
    prototype_description = fields.Text(string="Description")
    internal_note = fields.Text(string="Description")
    
    prototype_tech_pack = fields.Binary(string="Tech Pack")
    prototype_pattern = fields.Binary(string="Pattern")
    
    prototype_stages = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('qa', 'QA'),
        ('client_testing', 'Client Testing'),
        ('approved', 'Approved'),
        ('cancel', 'Cancel'),
        ],default='draft')
    check_status = fields.Boolean(string="Check Status")


    @api.multi
    def approve_wizard(self):
        product_prototype = self.env['product.prototype']
        current_id = self.env['product.prototype'].browse(self._context.get('active_ids'))

        self.prod_name =  current_id.prod_name
        self.prototype_product_catagory = current_id.prototype_product_catagory

        if self.check_status:
            data = {
            'prod_name' : self.prod_name,
            'prototype_order_date' : self.prototype_order_date,
            'prototype_customer_name' : self.prototype_customer_name.id,
            'prototype_development_request' : self.prototype_development_request.id,
            'prototype_bill' : self.prototype_bill.id,
            'prototype_description' : self.prototype_description,
            'internal_note' : self.internal_note,
            'prototype_tech_pack' : self.prototype_tech_pack,
            'prototype_pattern' : self.prototype_pattern,
            'prototype_product_catagory': self.prototype_product_catagory.id
            }
            product_prototype.create(data)
            current_id.prototype_stages = "cancel"

    @api.onchange('check_status')
    def check_status_onchange(self):
        current_id = self.env['product.prototype'].browse(self._context.get('active_ids'))
        if self.check_status:
            self.prod_name =  current_id.prod_name
            self.prototype_order_date = current_id.prototype_order_date
            self.prototype_customer_name = current_id.prototype_customer_name
            self.prototype_development_request = current_id.prototype_development_request
            self.prototype_bill = current_id.prototype_bill
            self.prototype_description = current_id.prototype_description
            self.internal_note = current_id.internal_note
            self.prototype_tech_pack = current_id.prototype_tech_pack
            self.prototype_pattern = current_id.prototype_pattern
            self.prototype_product_catagory = current_id.prototype_product_catagory

class project_management(models.Model): 
    _name = 'project.product'
    _rec_name = 'project'

    customer = fields.Many2one('res.partner', required= True, string="Customer Name")

    project = fields.Char(string="Project", required= True)

class development_attribute(models.Model): 
    _name = 'development.attribute'
    _inherit = 'product.attribute.line'

    attribute_development = fields.Many2one('product.portfolio')

    @api.onchange('attribute_id')
    def check_status_onchange(self):
        if self.attribute_id:
            self.product_tmpl_id = self.env['product.template'].search([])[0]

class prototype_attribute(models.Model): 
    _name = 'prototype.attribute'
    _inherit = 'product.attribute.line'

    # attribute_id = fields.Many2one('product.attribute')
    # product_tmpl_id = fields.Many2one('product.template')
    # value_ids = fields.Many2one('product.attribute.value')

    attribute_development = fields.Many2one('product.prototype')

    @api.onchange('attribute_id')
    def check_status_onchange(self):
        if self.attribute_id:
            self.product_tmpl_id = self.env['product.template'].search([])[0]