# -*- coding:utf-8 -*-
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
   # along with this program.  If not, see <http://www.g//nu.org/licenses/>.
#
##############################################################################
from openerp import models, fields, api
from datetime import date

class InwardGatepass(models.AbstractModel):
    _name = 'report.inward_gatepass.inward_gatepass_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('inward_gatepass.inward_gatepass_report')

        active_wizard = self.env['inward.gatepass'].search([])

        emp_list = []
        for x in active_wizard:
            emp_list.append(x.id)
        emp_list = emp_list
        emp_list_max = max(emp_list) 

        record_wizard = self.env['inward.gatepass'].search([('id','=',emp_list_max)])
        record_wizard_del = self.env['inward.gatepass'].search([('id','!=',emp_list_max)])
        record_wizard_del.unlink()

        name = record_wizard.name
        to = record_wizard.to
        code = record_wizard.code
        return_able = record_wizard.return_able
        category = record_wizard.category
        store = record_wizard.store
        requesition = record_wizard.requesition
        issue_date = record_wizard.issue_date
        carrier = record_wizard.carrier
        vechicle = record_wizard.vechicle
        status = record_wizard.status
        prepaid = record_wizard.prepaid
        approved = record_wizard.approved
        tree = []
        for x in record_wizard.tree_link_id:
            tree.append(x)



        def call_heading():
            if name == 'inwardgatepass':
                return "Inward Gatepass"
                
            if name == 'outwardgatepass':
                return "Outward Gatepass"
                

        docargs = {
            'doc_ids': docids,
            'doc_model': 'inward.gatepass',
            'data': data,
            'name': name,
            'to': to,
            'code':code,
            'return_able':return_able,
            'category':category,
            'store':store,
            'requesition':requesition,
            'issue_date':issue_date,
            'carrier':carrier,
            'vechicle':vechicle,
            'status':status,
            'tree' : tree,
            'prepaid': prepaid,
            'approved': approved,
            'call_heading':call_heading
             }

        return report_obj.render('inward_gatepass.inward_gatepass_report', docargs)