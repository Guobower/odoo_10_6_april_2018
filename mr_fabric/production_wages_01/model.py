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

class Mrfabricsheet(models.AbstractModel):
    _name = 'report.production_wages_01.mrfabricsheet_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('production_wages_01.mrfabricsheet_report')
        active_wizard = self.env['mrfabric.sheet'].search([])

        emp_list = []
        for x in active_wizard:
            emp_list.append(x.id)
        emp_list = emp_list
        emp_list_max = max(emp_list) 

        record_wizard = self.env['mrfabric.sheet'].search([('id','=',emp_list_max)])
        record_wizard_del = self.env['mrfabric.sheet'].search([('id','!=',emp_list_max)])
        record_wizard_del.unlink()

        work_order = record_wizard.work_order
        work = record_wizard.work_order.id
        production = record_wizard.production
        prod = record_wizard.production.id
        form = record_wizard.date_from
        to = record_wizard.date_to

        
        if work == False and prod == False:
            records = self.env['wage.per.piece'].search([('form','>=',form),('form','<=',to),('to','<=',to)])
        
        if work != False and prod == False:
            records = self.env['wage.per.piece'].search([('form','>=',form),('form','<=',to),('to','<=',to),('won.id','<=',work)])
        
        if work == False and prod != False:
            records = self.env['wage.per.piece'].search([('form','>=',form),('form','<=',to),('to','<=',to),('production.id','<=',prod)])
        
        if work != False and prod != False:
            records = self.env['wage.per.piece'].search([('form','>=',form),('form','<=',to),('to','<=',to),('production.id','<=',prod),('won.id','<=',work)])  


        def get_qty(attr,req):
            qty = 0
            dzn = 0
            for x in attr.tree_link:
                qty = qty + x.qty
            if req == 'qty':
                return int(qty)
            if req == 'dzn':
                dzn = qty / 12
                return int(dzn)

        def get_rate(attr):
            rate = 0 
            for x in attr.tree_link:
                rate = rate + x.rate
                return int(rate)

        def get_amount(attr):
            amount = 0 
            for x in attr.tree_link:
                amount = amount + x.amount
                return int(amount)


        docargs = {
            'doc_ids': docids,
            'doc_model': 'hr.employee',
            'work_order' : work_order,
            'production' : production,
            'form' : form,
            'to' : to,
            'records' : records,
            'get_qty' : get_qty,
            'get_rate' : get_rate,
            'get_amount' : get_amount
            }

        return report_obj.render('production_wages_01.mrfabricsheet_report', docargs)