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
    _name = 'report.costing_report.module_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('costing_report.module_report')
        records = self.env['product.prototype'].browse(docids)

        emp_list = []
        for x in records.prototype_cost:
            if x.type_of_work not in emp_list:
                emp_list.append(x.type_of_work)
        
        required_records = []
        def record_iteration(record_name):
            del required_records[:]
            for y in  records.prototype_cost:
                if y.type_of_work == record_name:
                    required_records.append(y)
        
        outter_shell = []
        def outter_cost():
            del outter_shell[:]
            for y in  records.prototype_cost:
                if y.type_of_work == "outter_shell":
                    outter_shell.append(y.cost)
            outter_cost = 0
            for x in outter_shell:
                outter_cost = outter_cost + x
            return outter_cost
        
        inner_shell = []
        def inner_cost():
            del inner_shell[:]
            for y in  records.prototype_cost:
                if y.type_of_work == "inside":
                    inner_shell.append(y.cost)
            inner_cost = 0
            for x in inner_shell:
                inner_cost = inner_cost + x
            return inner_cost
        
        accessories = []
        def access_cost():
            del accessories[:]
            for y in  records.prototype_cost:
                if y.type_of_work == "accessories":
                    accessories.append(y.cost)
            access_cost = 0
            for x in accessories:
                access_cost = access_cost + x
            return access_cost
        
        makery = []
        def makery_cost():
            del makery[:]
            for y in  records.prototype_cost:
                if y.type_of_work == "makery":
                    makery.append(y.cost)
            makery_cost = 0
            for x in makery:
                makery_cost = makery_cost + x
            return makery_cost
        
        def total_cost():
            total_cost = 0
            freight = records.freight
            total_cost = inner_cost() + outter_cost() + access_cost() + makery_cost() +freight
            return total_cost


        docargs = {
            'doc_ids': docids,
            'doc_model': 'product.prototype',
            'docs': records,
            'data': data,
            'heads': emp_list,
            'record_list': required_records,
            'record_iteration': record_iteration,
            'outter_cost': outter_cost,
            'inner_cost': inner_cost,
            'access_cost': access_cost,
            'makery_cost': makery_cost,
            'total_cost': total_cost
            }

        return report_obj.render('costing_report.module_report', docargs)




