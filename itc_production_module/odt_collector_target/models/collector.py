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


class Collector(models.Model):
    _name = 'money.collector'

    name = fields.Char('Name')
    payment_line_ids = fields.One2many('account.voucher', 'collector_id', 'Payment Details')
    collector_target_ids = fields.One2many('collector.target', 'collector_id', 'Collector Target')
