# -*- coding: utf-8 -*-
# 
#    OpenERP, Open Source Management Solution

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

from openerp import models, fields, api, _, tools
from datetime import datetime, timedelta

class SalesManTarget(models.Model):
    _name = 'sales.man.target'

    @api.depends('user_id', 'product_id', 'target_amount',)
    @api.one
    def _get_current(self):
        sale_order_obj = self.env['sale.order']
        for record in self:
            order_domain = [('user_id', '=', record.user_id.id),
                            ('date_order', '>=', record.from_date),
                            ('date_order', '<=', record.to_date)
                            ]
            amount = 0
            sale_order_list = sale_order_obj.search(order_domain)
            for order in sale_order_list:
                if record.product_id:
                    for line in order.order_line:
                        print "1", record.product_id, line.product_id
                        if record.product_id and line.product_id.id == record.product_id.id:
                            amount += line.price_subtotal
                else:
                    amount += order.amount_total
            record.current_amount = amount
            remaining_amount = record.target_amount - amount
            if remaining_amount >0:
                record.remaining_amount = remaining_amount
            if record.target_amount:
                record.progress = round(min(100.0 * amount / record.target_amount, 99.99), 2)

    # @api.one
    # @api.depends('current_amount', 'remaining_amount')
    # def _get_current1(self):
    #     for record in self:
    #         record.current_amount1 = record.current_amount

    user_id = fields.Many2one('res.users', 'Sales Man', ondelete='cascade', required=True)
    product_id = fields.Many2one('product.product', 'Product')
    target_amount = fields.Float('Target Amount')
    current_amount = fields.Float('Current Amount', compute='_get_current', store=False)
    # current_amount1 = fields.Float('Current Amount', compute='_get_current1', store=True)
    remaining_amount = fields.Float('Remaining Amount', compute='_get_current')
    progress = fields.Float('Progress', compute='_get_current')
    from_date = fields.Date('From Date', required=True)
    to_date = fields.Date('To Date', required=True)
