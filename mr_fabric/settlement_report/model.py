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
from dateutil.relativedelta import relativedelta
from datetime import date,datetime

class leavecashment(models.AbstractModel):
    _name = 'report.settlement_report.leave_cashment_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('settlement_report.leave_cashment_report')
        records = self.env['settlement'].browse(docids)

        # print records.date_app
        # print type(date(records.date_resign))
        if records.date_app and records.date_resign:
            y,m,d = records.date_app.split("-")
            app = datetime(int(y), int(m), int(d))
            x,y,z = records.date_resign.split("-")
            resign = datetime(int(x), int(y), int(z))
            year = relativedelta(resign,app).years
            month =relativedelta(resign,app).months
            days = relativedelta(resign,app).days
        else:
            year = 0
            month = 0
            days = 0

        

        docargs = {
            'doc_ids': docids,
            'doc_model': 'settlement',
            'docs': records,
            'year': year,
            'month': month,
            'days': days,

            }

        return report_obj.render('settlement_report.leave_cashment_report', docargs)