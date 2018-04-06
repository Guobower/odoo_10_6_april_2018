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
    _name = 'report.employee_details.module_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('employee_details.module_report')
        records = self.env['hr.employee'].browse(docids)

        refer = []
        for x in records.emp_link:
            if x.main == True:
                refer.append(x)

        def get_name():
            name = ""
            for x in refer:
                name = x.name 

            return name

        def get_cnic():
            cnic = ""
            for x in refer:
                cnic = x.cnic 

            return cnic

        def get_cnt():
            cnt = ""
            for x in refer:
                cnt = x.e_contact 

            return cnt

        def get_paddrs():
            add = ""
            for x in refer:
                add = x.per_address

            return add

        def get_taddrs():
            tadd = ""
            for x in refer:
                tadd = x.tem_address

            return tadd


        docargs = {
            'doc_ids': docids,
            'doc_model': 'hr.employee',
            'docs': records,
            'data': data,
            'refer': refer,
            'get_name': get_name,
            'get_cnic': get_cnic,
            'get_cnt': get_cnt,
            'get_paddrs': get_paddrs,
            'get_taddrs': get_taddrs,
            }

        return report_obj.render('employee_details.module_report', docargs)