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
    _name = 'report.sample_development.module_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('sample_development.module_report')
        records = self.env['product.prototype'].browse(docids)

        emp_list = []
        for x in records:
            if x.prototype_customer_name.name not in emp_list:
                emp_list.append(x.prototype_customer_name.name)
        
        required_records = []
        def record_iteration(record_name):
            del required_records[:]
            for y in  records:
                if y.prototype_customer_name.name == record_name:
                    required_records.append(y)

        def getdate():
            dater = date.today().strftime('%Y-%m-%d')
            return dater

        docargs = {
            'doc_ids': docids,
            'doc_model': 'product.prototype',
            'docs': records,
            'data': data,
            'employee': emp_list,
            'record_list': required_records,
            'record_iteration': record_iteration,
            'getdate': getdate
            }

        return report_obj.render('sample_development.module_report', docargs)




