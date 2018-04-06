# #-*- coding:utf-8 -*-
# ##############################################################################
# #
# #    OpenERP, Open Source Management Solution
# #    Copyright (C) 2011 OpenERP SA (<http://openerp.com>). All Rights Reserved
# #
# #    This program is free software: you can redistribute it and/or modify
# #    it under the terms of the GNU Affero General Public License as published by
# #    the Free Software Foundation, either version 3 of the License, or
# #    (at your option) any later version.
# #
# #    This program is distributed in the hope that it will be useful,
# #    but WITHOUT ANY WARRANTY; without even the implied warranty of
# #    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# #    GNU Affero General Public License for more details.
# #
# #    You should have received a copy of the GNU Affero General Public License
# #    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# #
# ##############################################################################
from odoo import models, fields, api

class StockMovementAddaReport(models.Model):
	_name = "stock.movement.addas"

	form = fields.Date(string="From")
	to = fields.Date(string="To")
	adda_field = fields.Many2one('adda',string="Adda")
	mill = fields.Many2one('product.product', string="Mill")
	party = fields.Many2one('res.partner', string="Party")
	tranfers = fields.Float(string="Total Tranfers")
	loadings = fields.Float(string="Total Loadings")

	stock_tree = fields.One2many('stock.movement.tree', "tree_link")

	@api.multi
	def genrate_lines(self):
		active_wizard = self.env['stock.movement.tree'].search([])
		active_wizard.unlink()

		transfers = self.env['loading.sugar.tree'].search([('date','>=',self.form),('date','<=',self.to),('adda.id','=',self.adda_field.id),('mill.id','=',self.mill.id),('transfer_type','=','g2c'),('party.id','=',self.party.id)])

		loadings = self.env['loading.adda.tree'].search([('adda.id','=',self.adda_field.id),('mill.id','=',self.mill.id),('party.id','=',self.party.id)])

		for x in loadings:

			lines = self.env['stock.movement.tree'].create({
				
			'date': x.date,
			'qty': x.qty,
			'adda': x.adda.id,
			'mill_loaded': x.mill_loaded.id,
			'destination': x.destination,
			'vehicle': x.vehicle_no,
			'billty': x.billty_no,
			'tree_link': self.id,
			'type_transfer': "out",
		})

		for x in transfers:

			lines = self.env['stock.movement.tree'].create({
				
			'date': x.date,
			'qty': x.qty,
			'adda': x.adda.id,
			'tree_link': self.id,
			'type_transfer': "in",
		})

		stockin = 0
		stockout = 0
		for x in self.stock_tree:
			if x.type_transfer == 'out':
				stockout = stockout + x.qty
			if x.type_transfer == 'in':
				stockin = stockin + x.qty

		self.tranfers = stockin
		self.loadings = stockout

class StockMovementAddaReportTree(models.Model):
	_name = "stock.movement.tree"

	date = fields.Date(string="Date")
	qty = fields.Float(string="Quantity")
	adda = fields.Many2one("adda",string="Adda")
	mill_loaded = fields.Many2one("res.partner",string="Mill Loaded")
	destination = fields.Char(string="Destination")
	vehicle = fields.Char(string="Vehicle No.")
	billty = fields.Char(string="Billty No.")
	type_transfer = fields.Selection([
		('out', 'Stock Out'),
		('in', 'Stock In'),
		],string = "Transfer Type")

	tree_link = fields.Many2one("stock.movement.addas")