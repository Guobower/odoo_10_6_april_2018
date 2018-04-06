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
###################################################
from openerp import models, fields, api

class SampleDevelopmentReport(models.AbstractModel):
    _name = 'report.omer_customer_invoice.module_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('omer_customer_invoice.module_report')
        records = self.env['ufc.auto'].browse(docids)
        users = self.env['res.users'].search([])

        def getbranch(atrrb):
            active_user = self._uid

            for x in users:
                if active_user == x.id:
                    if atrrb == "Address":
                        return x.Branch.Address
                    if atrrb == "Phone":
                        return x.Branch.Phone
                    if atrrb == "Ptcl":
                        return x.Branch.ptcl


        def namer():
            print "--------------"
            prov = ""
            for x in records:
                if x.customer.name == "ORIENT ELECTRONICS":
                    prov = x.customer.name
                if x.customer.name == "FFC Goth Machi":
                    prov = x.customer.name
                if x.customer.name == "FFC Mir Pur Mathelo":
                    prov = x.customer.name
                if x.customer.name == "Engro Fertilizer Dharki":
                    prov = x.customer.name
                if x.customer.name == "Engro Port Karachi":
                    prov = x.customer.name


            return prov

            
            

        docargs = {
            'doc_ids': docids,
            'doc_model': 'ufc.auto',
            'docs': records,
            'data': data,
            'getbranch': getbranch,
            'namer': namer
            }

        return report_obj.render('omer_customer_invoice.module_report', docargs)