#-*- coding:utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011 OpenERP SA (<http://openerp.com>). All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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
from datetime import date


class SampleDevelopmentReport(models.AbstractModel):
    _name = 'report.shipping_insructions.module_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('shipping_insructions.module_report')
        records = self.env['account.invoice'].browse(docids)
        invoices = self.env['commercial.packing.list'].search([('invoice_no','=',records.number)])
        invoice_cn=invoices.cn
        invoice_cn_date=invoices.cn_date
        gw=invoices.gross_weight
        nw=invoices.net_weight
        cs=invoices.carton_size

    # def get_gw(attr):
    #     inv_num=attr
    #     print "xxxxxxxxxxxxxxxxxx"
    #     print inv_num
    #     print "xxxxxxxxxxxxxxxxxx"
    #     invoices = self.env['commercial.packing.list'].search([('invoice_no','=',inv_num)])
    #     return invoices.gross_weight

    # def get_nw(attr):
    #     inv_num=attr
    #     print "xxxxxxxxxxxxxxxxxx"
    #     print inv_num
    #     print "xxxxxxxxxxxxxxxxxx"
    #     invoices = self.env['commercial.packing.list'].search([('invoice_no','=',inv_num)])
    #     return invoices.net_weight


        docargs = {
            'doc_ids': docids,
            'doc_model': 'account.invoice',
            'docs': records,
            'data': data,
            'cn': invoice_cn,
            'cn_date':invoice_cn_date,
            'nw':nw,
            'gw':gw,
            'cs':cs         
             }

        return report_obj.render('shipping_insructions.module_report', docargs)
