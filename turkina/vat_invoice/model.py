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

class PacificCommercialInvoice(models.AbstractModel):
    _name = 'report.vat_invoice.vat_invoice_id'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('vat_invoice.vat_invoice_id')
        records = self.env['account.invoice'].browse(docids)
        amt = 0.0
        actualAmt = 0.0
        for x in records.invoice_line_ids:
            amt = amt + ((x.discount/100) * x.price_unit * x.quantity)
            actualAmt = actualAmt + (x.price_unit * x.quantity)
        
        docargs = {
            'doc_ids': docids,
            'doc_model': 'account.invoice',
            'docs': records,
            'data': data,
            'amt': amt,
            'actualAmt': actualAmt,
            }

        return report_obj.render('vat_invoice.vat_invoice_id', docargs)