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
    _name = 'report.dharki_punjab_sales_tax_invoice.module_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('dharki_punjab_sales_tax_invoice.module_report')
        print "------------------------------------------0"
        records = self.env['summary.ffc'].browse(docids)
        for x in records:
            enteries = []
            if x.Customer.name == "Engro Fertilizer Dharki":
                print "mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm"
                for data in records.sum_ids2:
                    if data.province == "pun":
                        enteries.append(data)


        def freight():
            weight = 0
            for z in records.sum_ids2:
                if z.additional_freight == 60 and z.province == "pun":
                    weight = weight + z.weight 

            return weight


        def rate():
            value = 0
            for z in records.sum_ids2:
                if z.additional_freight == 50 and z.province == "pun":
                    value = value + z.weight 

            return value


        def enter():
            count = 0
            for amt in records.sum_ids2:
                if amt.via == 'kot':
                    count = count + 1

            return count


        def number():
            numb = 0
            for amt in records.sum_ids2:
                if amt.via == 'kash':
                    numb = numb + 1

            return numb

            

        lists = []
        for line in records.value_ids:
            if line.province == "pun":
                lists.append(line)


                           

        docargs = {
            'doc_ids': docids,
            'doc_model': 'summary.ffc',
            'docs': records,
            'data': data,
            'enteries': enteries,
            'freight': freight,
            'rate': rate,
            'enter': enter,
            'number': number,
            'lists' : lists

            }

        return report_obj.render('dharki_punjab_sales_tax_invoice.module_report', docargs)