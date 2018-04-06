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


class PurchaseORder(models.Model):
    _inherit = 'purchase.order'

    @api.one
    @api.depends('receipt_date', 'date_approve')
    def _get_duration(self):
        if self.receipt_date and self.date_approve:
            time_delta = (datetime.strptime(self.receipt_date, '%Y-%m-%d') - \
                                datetime.strptime(self.date_approve,'%Y-%m-%d'))
            hours, remainder = divmod(time_delta.total_seconds(), 3600)
            self.purchase_duration = hours

    @api.depends('picking_ids')
    @api.one
    def _get_receipt_date(self):
        date_list = []
        for picking in self.picking_ids:
            date_list.append(picking.date)
        if date_list:
            self.receipt_date = min(date_list)

    purchase_duration = fields.Float('Delivery Duration(Hours)', compute='_get_duration',
                                     help='Duration between approve date and Receipt date')
    receipt_date = fields.Date('Receipt Date', compute='_get_receipt_date')