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
    _name = 'report.region_bill_detail.module_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('region_bill_detail.module_report')
        active_wizard = self.env['region.wise.detail'].search([])
        emp_list = []
        for x in active_wizard:
            emp_list.append(x.id)
        emp_list = emp_list
        emp_list_max = max(emp_list) 

        record_wizard = self.env['region.wise.detail'].search([('id','=',emp_list_max)])

        record_wizard_del = self.env['region.wise.detail'].search([('id','!=',emp_list_max)])
        record_wizard_del.unlink()
        
        records = self.env['summary.ffc'].search([('Customer','=',record_wizard.customer.id)])
        for x in records:
            if x.Customer.name == "FFC Mir Pur Mathelo":
                enteries = []
                for x in records.sum_ids2:
                    if record_wizard.form <= x.invoice_date and record_wizard.to >= x.invoice_date and record_wizard.region == x.region:
                        if x not in enteries:
                            enteries.append(x)
                            
        for x in records:
            if x.Customer.name == "FFC Goth Machi":
                enteries = []
                for x in records.sum_ids2:
                    if record_wizard.form <= x.invoice_date and record_wizard.to >= x.invoice_date and record_wizard.region == x.region and record_wizard.types == x.types:
                        if x not in enteries:
                            enteries.append(x)
            
        
        

        def namer():
            print "--------------"
            prov = ""
            for x in records:
                if x.Customer.name == "FFC Goth Machi":
                    prov = x.Customer.name
                if x.Customer.name == "FFC Mir Pur Mathelo":
                    prov = x.Customer.name
            
            return prov



        codes = []
        for x in enteries:
            if x.code not in codes:
                codes.append(x.code)
        codes.sort(key=int)
        print codes
        print "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
       
        sorted_records = []
        for x in codes:
            for y in enteries:
                if y.code == x:
                    sorted_records.append(y)
        print sorted_records
        print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"


        # def custm():
        #     print "88888888888888888888888888888888888888888888888"
        #     name = ""
        #     for data in records:
        #         print records
        #         print "88888888888888888888888888888888888888888888888"
        #         if data.Customer == "FFC Goth Machi":
        #             name = data.Customer
        #             print name
        #             print "000000000000000000000000000000000000000000000"
        #         if data.Customer == "FFC Mir Pur Mathelo":
        #             name = data.Customer
        #             print name
        #             print "000000000000000000000000000000000000000000000"

        #     return name


        region = record_wizard.region.name
        customer = record_wizard.customer.name
        form = record_wizard.form
        to = record_wizard.to
        types = record_wizard.types


      

        docargs = {
            'doc_ids': docids,
            'doc_model': 'summary.ffc',
            'docs': records,
            'data': data,
            'enteries': enteries,
            'namer': namer,
            'sorted_records': sorted_records,
            'region': region,
            'customer': customer,
            'form': form,
            'to': to,
            'types': types
            }

        return report_obj.render('region_bill_detail.module_report', docargs)