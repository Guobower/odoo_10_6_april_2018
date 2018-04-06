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

from openerp import models, fields, api, _
from datetime import datetime, timedelta


class ProductTarget(models.Model):
    _name = 'product.target'


    @api.depends('product_id', 'from_date', 'to_date', 'current_qty', 'target_qty')
    @api.one
    def _get_progress(self):
        sale_order_line_obj = self.env['sale.order.line']
        for record in self:
            doamin = [('product_id','in', [record.product_id.product_variant_ids.id]),
                      ('date_order','>=',record.from_date),
                      ('date_order', '<=', record.to_date)
                     ]
            qty  = 0
            sale_lines=sale_order_line_obj.search(doamin)
            for line in sale_lines:
                qty+= line.product_uom_qty
            record.current_qty = qty
            if record.target_qty:
                record.progress = round(min(100.0 * qty / record.target_qty, 99.99), 2)

    product_id = fields.Many2one('product.template', 'Product', ondelete='cascade')
    target_qty = fields.Float('Target Qty')
    current_qty = fields.Float('Desired Qty', compute='_get_progress', store=False)
    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date')
    progress = fields.Float('Target Progress', compute='_get_progress')


