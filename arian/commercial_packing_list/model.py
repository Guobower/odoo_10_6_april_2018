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
    _name = 'report.commercial_packing_list.module_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('commercial_packing_list.module_report')
        records = self.env['commercial.packing.list'].browse(docids)

        entries = []

        for x in records.commercial_packing_list_tree_link:
            if x.carton not in entries:
                entries.append(x.carton)

        active_record = []
        def get_values(prod_id,attr):
            del active_record[:]
            product = prod_id
            for x in records.commercial_packing_list_tree_link:
                if x.carton == product:
                    active_record.append(x)

            if attr == 'qty_cartons':
                total_qty = 0
                for x in active_record:
                    total_qty = total_qty + x.qty

                return total_qty

            if attr == 'color':
                prod_color = ' '
                color_list = []
                for x in active_record:
                    if prod_color == ' ':
                        color_list.append(x.colour.name)
                        prod_color = x.colour.name
                    else:
                        if x.colour.name not in color_list:
                            color_list.append(x.colour.name)
                            prod_color = prod_color + ', ' + x.colour.name

                return prod_color

            if attr == 'net_weight':
                net_weight = 0
                for x in active_record:
                    if x.net_weight != 0:
                        net_weight = x.net_weight

                return net_weight


            if attr == 'gross_weight':
                gross_weight = 0
                for x in active_record:
                    if x.gross_weight != 0:
                        gross_weight = x.gross_weight

                return gross_weight

            if attr == 'volume':
                volumed = 0
                for x in active_record:
                    if x.volume != 0:
                        volumed = x.volume

                return volumed

        activities = []
        sizes = []
        def sizer(prod_id,prod_catg,attr):
            del activities[:]
            del sizes[:]
            sized = ' '
            product = prod_id
            for x in records.commercial_packing_list_tree_link:
                if x.carton == product:
                    activities.append(x)

            if attr == 'size':
                for x in activities:
                    sizes.append(x.size.name)

                count = 0
                for x in sizes:
                    if count == prod_catg:
                        sized = sizes[count]
                    count = count + 1

                return sized

            if attr == 'qty':
                for x in activities:
                    sizes.append(x.qty)

                count = 0
                for x in sizes:
                    if count == prod_catg:
                        sized = sizes[count]
                    count = count + 1

                return sized

            if attr == 'des':
                for x in activities:
                    sizes.append(x.des)

                count = 0
                for x in sizes:
                    if count == prod_catg:
                        sized = sizes[count]
                    count = count + 1

                return sized

            if attr == 'artical':
                for x in activities:
                    sizes.append(x.artical_no.artical_num)

                count = 0
                for x in sizes:
                    if count == prod_catg:
                        sized = sizes[count]
                    count = count + 1

                return sized



        docargs = {
            'doc_ids': docids,
            'doc_model': 'commercial.packing.list',
            'docs': records,
            'data': data,
            'entries': entries,
            'get_values': get_values,
            'active_record': active_record,
            'sizes': sizes,
            'sizer': sizer
            }

        return report_obj.render('commercial_packing_list.module_report', docargs)