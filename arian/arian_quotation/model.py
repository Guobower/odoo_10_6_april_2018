# -*- coding: utf-8 -*- 
from odoo import models, fields, api

class order_quotation(models.Model): 
    _name = 'order.quotation'
    _rec_name = 'customer'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    quote_no = fields.Char(string="Quote #")
    proj_descrip = fields.Char(string="Quote/Project Description")

    customer = fields.Many2one('res.partner',string="Customer")

    dated = fields.Date("Dated")
    valid_until = fields.Date("Valid Until")

    data_comes = fields.One2many('quotation.tree','data_sends')

class order_quotation_tree(models.Model): 
    _name = 'quotation.tree'

    prod_name = fields.Many2one('product.product',string="Product")
    price = fields.Float(string="Price")

    data_sends = fields.Many2one('order.quotation')