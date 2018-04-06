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

class SampleDevelopmentReport(models.AbstractModel):
    _name = 'report.certificate_of_origin.module_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('certificate_of_origin.module_report')
        records = self.env['account.invoice'].browse(docids)
        invoices = self.env['commercial.packing.list'].search([('invoice_no','=',records.number)])
        gw=invoices.gross_weight
        nw=invoices.net_weight

        active_user = self._uid
        users = self.env['res.users'].search([('id','=',active_user)])
        company_name = ''
        street = ''
        street2 = ''
        city = ''
        state = ''
        country = ''
        for x in users:
            company_name = x.company_id.name
            street = x.company_id.street
            street2 = x.company_id.street2
            city = x.company_id.city
            state = x.company_id.state_id.name
            country = x.company_id.country_id.name


        
        docargs = {
            'doc_ids': docids,
            'doc_model': 'account.invoice',
            'docs': records,
            'company_name': company_name,
            'street': street,
            'street2': street2,
            'city': city,
            'state': state,
            'country': country,
            'gw':gw,
            'nw':nw

            }

        return report_obj.render('certificate_of_origin.module_report', docargs)