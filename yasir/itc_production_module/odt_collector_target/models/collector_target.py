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


class CollectorTarget(models.Model):
    _name = 'collector.target'


    # @api.depends('collector_id', 'from_date', 'to_date', 'current_amount', 'target_amount')
    # @api.one
    # def _get_progress(self):
    #     account_voucher_obj = self.env['account.voucher']
    #     for record in self:
    #         doamin = [('collector_id','=', record.id),
    #                   ('date','>=',record.from_date),
    #                   ('date', '<=', record.to_date)
    #                  ]
    #         amount = 0
    #         account_voucher=account_voucher_obj.search(doamin)
    #         for line in account_voucher:
    #             amount+= line.amount
    #         record.current_amount = amount
    #         if record.target_amount:
    #             record.progress = round(min(100.0 * amount / record.target_amount, 99.99), 2)

    collector_id = fields.Many2one('money.collector', 'Collector', ondelete='cascade')
    target_amount = fields.Float('Target Amount')
    current_amount = fields.Float('Current Amount')
    # current_amount = fields.Float('Current Amount', compute='_get_progress', store=False)
    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date')
    progress = fields.Float('Target Progress',)
    # progress = fields.Float('Target Progress', compute='_get_progress')


