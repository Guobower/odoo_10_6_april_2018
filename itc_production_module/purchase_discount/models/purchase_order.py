# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"


    @api.one
    @api.depends('price_subtotal', 'discount')
    def compute_net_amount(self):
        for line in self:
            line.total_amount = line.price_subtotal * (1 - line.discount/100)

    discount = fields.Float(
        string='Discount', digits_compute=dp.get_precision('Discount'))
    total_amount = fields.Float('Net Amount', compute=compute_net_amount)
    _sql_constraints = [
        ('discount_limit', 'CHECK (discount <= 100.0)',
         'Discount must be lower than 100%.'),
    ]


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.depends('amount_total','order_line.total_amount')
    def _compute_total(self):
        for order in self:
            total = 0
            cur = order.pricelist_id.currency_id
            for line in order.order_line:
                total += line.total_amount
            order.total_after_discount = cur.round(total)

    total_after_discount = fields.Float('Total After Discount', compute='_compute_total')


    # @api.model
    # def _prepare_inv_line(self, account_id, order_line):
    #     result = super(PurchaseOrder, self)._prepare_inv_line(
    #         account_id, order_line)

    #     result['discount'] = (order_line.discount / (order_line.price_unit * order_line.product_qty)) * 100 if order_line.price_unit and order_line.product_qty else 0

    #     return result

    # @api.model
    # def _prepare_order_line_move(self, order, order_line, picking_id,
    #                              group_id):
    #     res = super(PurchaseOrder, self)._prepare_order_line_move(
    #         order, order_line, picking_id, group_id)
    #     for vals in res:
    #         vals['price_unit'] = (vals.get('price_unit', 0.0) *
    #                               (1 - order_line.discount))
    #     return res
