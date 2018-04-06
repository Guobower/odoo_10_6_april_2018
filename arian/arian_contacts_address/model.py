# -*- coding: utf-8 -*- 
from odoo import models, fields, api

class addrerss_extension(models.Model): 
    _inherit = 'res.partner'

    name = fields.Char(string="Customer Name")

    contact_address = fields.One2many('address.contacts','address_contact_id')

class addrerss_contacts(models.Model): 
    _name = 'address.contacts'

    customer_name = fields.Char(string="Contact Name", required= True)
    job_position = fields.Char(string="Job Position", placeholder="eg. Manger")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    mobile = fields.Char(string="Mobile")
    address = fields.Char(string="Address")
    invoice_address = fields.Char(string="Invoice Address")
    shipping_address = fields.Char(string="Shipping Address")
    
    title = fields.Many2one('res.partner.title', string="Title");

    address_contact_id = fields.Many2one('res.partner')