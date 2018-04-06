# -*- coding: utf-8 -*- 
from odoo import models, fields, api
class product_extension(models.Model): 
    _inherit = 'product.template'

    article_num = fields.Many2one('product.artical',string="Article Number" )
    uom = fields.Many2one('product.uom',string="Unit of Measure" )
    customer_ref = fields.Char(string="Customer Reference No")
    bill_ref = fields.Char(string="Bill of Material Reference #")
    internal_ref = fields.Char(string="Item Code")
    inner_carton = fields.Char(string="Inner Carton")
    pcs_carton = fields.Char(string="Pcs/Carton")
    style_no = fields.Char(string="Style No.")
    hs_code = fields.Char(string="HS Code")
    composition = fields.Char(string="Composition")
    barcode = fields.Char(string="Bar Code")
    art_code = fields.Char(string="External Art Code")
    qty_on_hand = fields.Integer(string="Quantity On Hand")

    prod_customer = fields.Many2one('res.partner',string="Customer", domain=[('customer','=',True)] )

    length = fields.Float(string="Lenght")
    width = fields.Float(string="Width")
    height = fields.Float(string="Height")
    grossed_weight = fields.Float(string="Gross Weight (Gms)")
    size_from = fields.Float(string="Size From")
    size_to = fields.Float(string="Size to")
    carton_lenght = fields.Float(string="Lenght")
    carton_width = fields.Float(string="Width")
    carton_height = fields.Float(string="Height")
    carton_weight = fields.Float(string="Gross Weight (Gms)")
    carton_master_height = fields.Float(string="Height")
    material_descrip = fields.Text(string="Material for Description")
    workmanship_descrip = fields.Text(string="Description for Workmanship")
    decor_descrip = fields.Text(string="Description for Decor")
    packing_descrip = fields.Text(string="Description for Packing")
    prototype_tech_pack = fields.Binary(string="Tech Pack")
    prototype_pattern = fields.Binary(string="Pattern")
    
    net_weight = fields.Float(string="Net Weight (Gms)")
    carton_net_weight = fields.Float(string="Net Weight (Gms)")
    counted_volume = fields.Float("Vloume")
    counted_volume_2 = fields.Float("Vloume")

    @api.onchange('length','width','carton_master_height')
    def lwh(self):
        self.counted_volume = self.length * self.width * self.carton_master_height
            
    @api.onchange('carton_lenght','carton_width','carton_height')
    def c_lwh(self):
        self.counted_volume_2 = self.carton_lenght * self.carton_width * self.carton_height
            
    @api.onchange('prod_customer')
    def onchange_customer(self):
        if self.prod_customer:
            self.length = self.prod_customer.length
            self.width = self.prod_customer.width
            self.grossed_weight = self.prod_customer.weight
            self.size_from = self.prod_customer.size_from
            self.size_to = self.prod_customer.size_to
            self.carton_lenght = self.prod_customer.carton_lenght
            self.carton_width = self.prod_customer.carton_width
            self.carton_height = self.prod_customer.carton_height
            self.carton_weight = self.prod_customer.carton_weight
            self.inner_carton = self.prod_customer.inner_carton
            self.pcs_carton = self.prod_customer.pcs_carton
            self.carton_master_height = self.prod_customer.master_height
            self.volume = self.prod_customer.volume
            self.net_weight = self.prod_customer.net_weight
            self.counted_volume_2 = self.prod_customer.i_volume
            self.carton_net_weight = self.prod_customer.i_net_weight

    @api.multi
    def write(self, vals):
        result = super(product_extension, self).write(vals)

        for x in self.product_variant_ids:

            x.internal_ref = self.internal_ref
            x.article_num = self.article_num
            x.customer_ref = self.customer_ref
            x.bill_ref = self.bill_ref
            x.prod_customer = self.prod_customer
            x.style_no = self.style_no
            x.v_hs_code = self.hs_code
            x.v_composition = self.composition
            x.v_uom = self.uom
            x.m_length = self.length
            x.m_width = self.width
            x.m_height = self.carton_master_height
            x.m_volume = self.volume
            x.m_gross_weight = self.weight
            x.m_net_weight = self.net_weight
            x.m_size_from = self.size_from
            x.m_size_to = self.size_to
            x.m_inner_carton = self.inner_carton
            x.i_lenght = self.carton_lenght
            x.i_width = self.carton_width
            x.i_height = self.carton_height
            x.i_volume = self.counted_volume_2
            x.i_gross_weight = self.carton_weight
            x.i_net_weight = self.carton_net_weight
            x.i_pcs_carton = self.pcs_carton
        return result

class product_extension_varient(models.Model): 
    _inherit = 'product.product'

    article_num = fields.Many2one('product.artical',string="Article Number" )
    customer_ref = fields.Char(string="Customer Reference No")
    bill_ref = fields.Char(string="Bill of Material Reference #")
    internal_ref = fields.Char(string="Item Code")
    style_no = fields.Char(string="Style No.")

    prod_customer = fields.Many2one('res.partner',string="Customer", domain=[('customer','=',True)] )
    
    m_length = fields.Float(string="Lenght")
    m_width = fields.Float(string="Width")
    m_height = fields.Float(string="Height")
    m_volume=fields.Float("Vloume")
    m_gross_weight = fields.Float(string="Gross Weight (Gms)")
    m_net_weight = fields.Float(string="Net Weight (Gms)")
    m_size_from = fields.Float(string="Size From")
    m_size_to = fields.Float(string="Size to")
    m_inner_carton=fields.Char("Inner Carton")

    i_lenght = fields.Float(string="Lenght")
    i_width = fields.Float(string="Width")
    i_height = fields.Float(string="Height")
    i_volume=fields.Float("Vloume")
    i_gross_weight = fields.Float(string="Gross Weight (Gms)")
    i_net_weight = fields.Float(string="Net Weight (Gms)")
    i_pcs_carton=fields.Char("Pcs/Carton")

    v_hs_code = fields.Char(string="HS Code")
    v_barcode = fields.Char(string="Bar Code")
    v_composition = fields.Char(string="Composition")
    v_uom = fields.Many2one('product.uom',string="Unit of Measure" )
    # @api.model
    # def create(self, vals):
    #     new_record = super(product_extension_varient, self).create(vals)
    #     new_record.internal_ref = new_record.product_tmpl_id.internal_ref
    #     new_record.article_num = new_record.product_tmpl_id.article_num
    #     new_record.customer_ref = new_record.product_tmpl_id.customer_ref
    #     new_record.bill_ref = new_record.product_tmpl_id.bill_ref
    #     new_record.prod_customer = new_record.product_tmpl_id.prod_customer
    #     new_record.style_no = new_record.product_tmpl_id.style_no
    #     return

class artical(models.Model): 
    _name = 'product.artical'
    _rec_name = 'artical_num'
    artical_num =fields.Char("Article No.")
