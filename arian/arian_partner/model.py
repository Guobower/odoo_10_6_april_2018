# -*- coding: utf-8 -*- 
from odoo import models, fields, api

class partner_extension(models.Model): 
    _inherit = 'res.partner' 

    forwarder = fields.Boolean()

    forwarder_name = fields.Many2one('res.partner',string="Forwarder Name", domain=[('forwarder','=',True)] )
    incoterms = fields.Many2one('stock.incoterms',string="Incoterms" )

    length = fields.Float(string="Lenght")
    width = fields.Float(string="Width")
    volume=fields.Float(string="Volume")
    net_weight=fields.Float(string="Net Weight (Gms)")
    volume=fields.Float(string="Volume")
    weight = fields.Float(string="Gross Weight (Gms)")
    size_from = fields.Float(string="Size From")
    size_to = fields.Float(string="Size to")
    carton_lenght = fields.Float(string="Lenght")
    carton_width = fields.Float(string="Width")
    carton_height = fields.Float(string="Height")
    i_net_weight=fields.Float(string="Net Weight (Gms)")
    i_volume=fields.Float(string="Volume")
    carton_weight = fields.Float(string="Gross Weight (Gms)")
    master_height = fields.Float(string="Height")

    inner_carton = fields.Char(string="Inner Carton")
    pcs_carton = fields.Char(string="Pcs/Carton")
    vendor_ref_no = fields.Char(string="Vendor Reference #") 
    ntn = fields.Char(string="NTN No") 


    @api.onchange('length','width','master_height')
    def lwh(self):
        if self.length>0 and self.width>0 and self.master_height>0:
            self.volume=self.length * self.width * self.master_height

        print "----------------------"
        print self.supplier
        print "----------------------"
            
    @api.onchange('carton_lenght','carton_width','carton_height')
    def c_lwh(self):
        if self.carton_lenght>0 and self.carton_width>0 and self.carton_height>0:
            self.i_volume=self.carton_lenght * self.carton_width * self.carton_height

class saleorder_extension(models.Model): 
    _inherit = 'sale.order' 

    @api.onchange('partner_id')
    def onchange_incoterm(self):
        if self.partner_id:
    	   self.incoterm = self.partner_id.incoterms.id

class stockincoterms_extension(models.Model): 
    _inherit = 'stock.incoterms'

    _rec_name = 'code' 