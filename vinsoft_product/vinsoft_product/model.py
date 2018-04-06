# -*- coding: utf-8 -*- 
from odoo import models, fields, api
from openerp.exceptions import Warning, ValidationError

class ProductTheme(models.Model): 
    _name = 'product.theme'
    _rec_name = 'name'
    _inherit = 'product.template'

    field1 = fields.Char(string="Código Producto")
    field2 = fields.Char(string="Código Producto")
    field3 = fields.Char(string="Código Producto")
    field4 = fields.Char(string="Código Producto")

    field5 = fields.Char(string="Código Producto")
    field6 = fields.Char(string="Código Producto")
    field7 = fields.Char(string="Código Producto")
    field8 = fields.Many2one('product.template',string="Código Producto")
    field9 = fields.Many2one('product.template',string="Código Producto")
    field10 = fields.Many2one('product.template',string="Código Producto")
    field11 = fields.Many2one('product.template',string="Código Producto")

    field12 = fields.Selection([('litros','Litros'),('centemeter','centimetros'),('pulgadas','pulgadas')])
    field13 = fields.Boolean(string="Código Producto")
    field14 = fields.Boolean(string="Código Producto")
    field15 = fields.Selection([('litros','Litros'),('centemeter','centimetros'),('pulgadas','pulgadas')])
    field16 = fields.Selection([('litros','Litros'),('centemeter','centimetros'),('pulgadas','pulgadas')])
    field17 = fields.Char(string="Descripción")
    field18 = fields.Selection([('litros','Litros'),('centemeter','centimetros'),('pulgadas','pulgadas')],string="Impuesto")
    field20 = fields.One2many('product.tree.one','field32')
    field21 = fields.Char(string="Descripción")
    field22 = fields.Char(string="Descripción")
    field23 = fields.Char(string="Descripción")
    field24 = fields.Many2one('product.template',string="Código Producto")
    field25 = fields.Many2one('product.template',string="Código Producto")
    field26 = fields.Many2one('product.template',string="Código Producto")
    field27 = fields.Text(string="Código Producto")
    pre_price = fields.Float(string ="Pre Price")
    curr_rate = fields.Many2one('ecube.currency',string="Currency")

    @api.onchange('curr_rate','pre_price')
    def _change_sale_price(self):
        if self.pre_price > 0:
            self.list_price = self.pre_price * self.curr_rate.rate

class EcubeCurrency(models.Model):
    _name = 'ecube.currency'

    name = fields.Char(string="Name")
    rate = fields.Float(string="Rate")

class ProductThemeTreeOne(models.Model): 
    _name = 'product.tree.one'

    field28 = fields.Char(string="Nombre Lista de Precio")
    field29 = fields.Float(string="Vigencia")
    field30 = fields.Float(string="Valor Neto")
    field31 = fields.Float(string="Valor Total")
    field32 = fields.Many2one('product.theme',string="Código Producto")

