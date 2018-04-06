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
from datetime import timedelta,datetime,date
from dateutil.relativedelta import relativedelta
import time

class SampleDevelopmentReport(models.AbstractModel):
    _name = 'report.stock_report.customer_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('stock_report.customer_report')
        active_wizard = self.env['stock.report'].search([])
        emp_list = []
        for x in active_wizard:
            emp_list.append(x.id)
        emp_list = emp_list
        emp_list_max = max(emp_list) 

        record_wizard = self.env['stock.report'].search([('id','=',emp_list_max)])

        record_wizard_del = self.env['stock.report'].search([('id','!=',emp_list_max)])
        record_wizard_del.unlink()
        date_from = record_wizard.date_from
        date_to = record_wizard.date_to
        product = record_wizard.product
        types = record_wizard.types
        records = self.env['saif.stock.tree'].search([])

        if types == "specfic":
            prod = []
            for x in product:
                prod.append(x)
                

        if types == "all":
            prod = []
            for z in records:
                if z.product not in prod:
                    prod.append(z.product)



        products = []
        def get_prod(attr):
            del products[:]
            rec = self.env['saif.stock.tree'].search([('date','>=',record_wizard.date_from),('date','<=',record_wizard.date_to)])
            for x in rec:
                if x.product.id == attr:
                    if x.date not in products:
                        products.append(x.date)
            products.sort(key=lambda x: x)


        def get_issued(attr,prod):
            value = 0
            rec = self.env['saif.stock.tree'].search([('date','>=',record_wizard.date_from),('date','<=',record_wizard.date_to)])
            for x in rec:
                if x.product.id == prod and x.date == attr:
                    value = value + x.issued

            return value


        def get_recevied(attr,prod):
            value = 0
            rec = self.env['saif.stock.tree'].search([('date','>=',record_wizard.date_from),('date','<=',record_wizard.date_to)])
            for x in rec:
                if x.product.id == prod and x.date == attr:
                    value = value + x.received

            return value


        def get_prev(prod):
            rec = 0
            issue = 0
            value = 0
            records = self.env['saif.stock.tree'].search([('date','<',record_wizard.date_from)])
            for x in records:
                if x.product.id == prod:
                    rec = rec + x.received
                    issue = issue + x.issued

            value = rec - issue

            return value


        
        docargs = {
        
            'doc_ids': docids,
            'doc_model': 'saif.stock',
            'docs': records,
            'prod':prod,
            'products':products,
            'get_prod':get_prod,
            'get_issued':get_issued,
            'get_recevied':get_recevied,
            'get_prev':get_prev,

            }

        return report_obj.render('stock_report.customer_report', docargs)