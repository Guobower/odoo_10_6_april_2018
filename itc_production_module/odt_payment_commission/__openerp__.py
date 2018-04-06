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
# -*- coding: utf-8 -*-
{
    'name': "SalesMan Payment Commission",
    'author': "OdooTec",
    'website': "www.odootec.com",
    'category': 'Accounting',
    'version': '1.0.1',
    'depends': [
        'mail', 'account_voucher'
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_voucher.xml',
        'report/payment_commission_report_view.xml'
        ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}

