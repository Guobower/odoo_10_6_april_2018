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

class costsheet(models.AbstractModel):
    _name = 'report.cost_sheet.cost_sheet_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('cost_sheet.cost_sheet_report')
        records = self.env['merchandising.costing'].browse(docids)

        firsts = []
        def firster(attr):
            del firsts[:]
            for x in attr:
                firsts.append(x)
                return

        lasts = []
        def laster(attr):
            del lasts[:]
            counter = 0
            for x in attr:
                if counter !=0:
                    lasts.append(x)
                counter = counter + 1

        def getfabrics(attr):
            value = 0
            for x in records.consumption_tree:
                if x.typed.fabric.id == attr.id:
                    value = value + float(x.consumption)

            return int(value)

        def getkgs(attr):
            value = 0
            total_yarn = 0

            for x in records.consumption_tree:
                if x.typed.fabric.id == attr.id:
                    value = value + float(x.consumption)

            for x in records.fabric_tree:
                if x.fabricno.id == attr.id:
                    total_yarn = total_yarn + x.total_yarn

            return int((value + total_yarn)/1000)


        docargs = {
            'doc_ids': docids,
            'doc_model': 'merchandising.costing',
            'docs': records,
            'firsts': firsts,
            'firster': firster,
            'lasts': lasts,
            'laster': laster,
            'getfabrics': getfabrics,
            'getkgs': getkgs
            }

        return report_obj.render('cost_sheet.cost_sheet_report', docargs)