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


class AccountVoucher(models.Model):
    _inherit = 'account.voucher'

    sales_man_commission = fields.Float('Sales Man Commission (%)')
    sales_man_id = fields.Many2one('res.users', 'Sales Man')

    # @api.multi
    # def proforma_voucher(self):
    #     res = super(AccountVoucher, self).proforma_voucher()
    #     commission_line_obj = self.env['payment.commission.line']
    #     amount = 0.00
    #     if self.sales_man_commission:
    #         amount = self.amount*(self.sales_man_commission/100)
    #     commission_line_obj.create({
    #         'user_id': self.sales_man_id.id,
    #         'amount': amount,
    #         'reference': self.name,
    #         'date': self.date
    #         })
    #     return res