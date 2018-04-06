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
    _name = 'report.carton_labels.module_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('carton_labels.module_report')
        records = self.env['commercial.packing.list'].browse(docids)

        
        def get_product(artical_no):
            artical = artical_no
            products = self.env['product.template'].search([('article_num','=',artical)])
            for x in products:
                return x.name

        entries = []
        for x in records:
            for y in x.commercial_packing_list_tree_link:
                if y.carton not in entries:
                    entries.append(y.carton)

        activities = []
        def sizer(prod_id,attr):
            del activities[:]
            product = prod_id
            for x in records.commercial_packing_list_tree_link:
                if x.carton == product:
                    activities.append(x)

            if attr == 'artical':

                prod_color = ' '
                color_list = []
                for x in activities:
                    if prod_color == ' ':
                        color_list.append(x.artical_no.artical_num)
                        prod_color = x.artical_no.artical_num
                    else:
                        if x.artical_no.artical_num not in color_list:
                            color_list.append(x.artical_no.artical_num)
                            prod_color = prod_color + ', ' + x.artical_no.artical_num
                return prod_color

            if attr == 'name':

                prod_color = ' '
                color_list = []
                for x in activities:
                    artical = get_product(x.artical_no.artical_num)
                    if prod_color == ' ':
                        color_list.append(artical)
                        prod_color = artical
                    else:
                        if artical not in color_list:
                            color_list.append(artical)
                            prod_color = prod_color + ', ' + artical
                return prod_color

            if attr == 'color':

                prod_color = ' '
                color_list = []
                for x in activities:
                    if prod_color == ' ':
                        color_list.append(x.colour.name)
                        prod_color = x.colour.name
                    else:
                        if x.colour.name not in color_list:
                            color_list.append(x.colour.name)
                            prod_color = prod_color + ', ' + x.colour.name
                return prod_color

            if attr == 'qty':

                quantity = 0
                for x in activities:
                    quantity = quantity + x.qty

                return quantity

        docargs = {
            'doc_ids': docids,
            'doc_model': 'commercial.packing.list',
            'docs': records,
            'data': data,
            'entries': entries,
            'sizer':sizer

            }

        return report_obj.render('carton_labels.module_report', docargs)