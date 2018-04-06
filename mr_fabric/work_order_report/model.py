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

class WorkOrderReport(models.AbstractModel):
    _name = 'report.work_order_report.work_order'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('work_order_report.work_order')
        active_wizard = self.env['workorder.report'].search([])

        emp_list = []
        for x in active_wizard:
            emp_list.append(x.id)
        emp_list = emp_list
        emp_list_max = max(emp_list) 

        record_wizard = self.env['workorder.report'].search([('id','=',emp_list_max)])
        record_wizard_del = self.env['workorder.report'].search([('id','!=',emp_list_max)])
        record_wizard_del.unlink()

        workorder = record_wizard.won

        yarn_dyeing = self.env['yarn.dyeing.tree'].search([('won.id','=',workorder.id)])
        fabric_dyeing = self.env['fabric.dyeing.tree'].search([('won.id','=',workorder.id)])
        fabric_knit = self.env['fabric.knitting.tree'].search([('won.id','=',workorder.id)])
        work_orders = self.env['mrp.production'].search([('id','=',workorder.id)])
        yarn_require = self.env['yarn.requirement.tree'].search([('won.id','=',workorder.id)])
        purchase_order = self.env['purchase.order.line'].search([('wo_no.id','=',workorder.id)])
        access_issue = self.env['purchase.access.issue'].search([('wo.id','=',workorder.id)])
        accessories = self.env['purchase.accessories.tree'].search([('wo_no.id','=',workorder.id)])

        docargs = {
            'doc_ids': docids,
            'doc_model': 'mrp.production',
            'data': data,
            'workorder': workorder,
            'yarn_dyeing': yarn_dyeing,
            'fabric_dyeing': fabric_dyeing,
            'fabric_knit': fabric_knit,
            'work_orders': work_orders,
            'yarn_require': yarn_require,
            'purchase_order': purchase_order,
            'access_issue': access_issue,
            'accessories': accessories,
            }

        return report_obj.render('work_order_report.work_order', docargs)