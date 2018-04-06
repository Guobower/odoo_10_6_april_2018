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
from num2words import num2words

class SampleDevelopmentReport(models.AbstractModel):
    _name = 'report.commercial_invoice_v4.module_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('commercial_invoice_v4.module_report')
        records = self.env['account.invoice'].browse(docids)

        active_user = self._uid
        users = self.env['res.users'].search([('id','=',active_user)])
        country = ''
        for x in users:
            country = x.company_id.country_id.name

        temple_ids = []
        for x in records.invoice_line_ids:
            if x.product_id.product_tmpl_id not in temple_ids:
                temple_ids.append(x.product_id.product_tmpl_id)

        temple_records = []
        def temple_products(prod_id, attrib):
            del temple_records[:]
            current_prod = prod_id
            for x in records.invoice_line_ids:
                if x.product_id.product_tmpl_id == prod_id:
                    temple_records.append(x)

            if attrib == "name":
                prod_name = ' '
                for x in temple_records:
                    prod_name = x.product_id.name
                return prod_name

            if attrib == "color":
                prod_color = ' '
                color_list = []
                for x in temple_records:
                    if x.product_id.product_tmpl_id == current_prod:
                        for y in x.product_id.attribute_value_ids:
                            if y.attribute_id.name == "Color":
                                if prod_color == ' ':
                                    color_list.append(y.name)
                                    prod_color = y.name
                                else:
                                    if y.name not in color_list:
                                        color_list.append(y.name)
                                        prod_color = prod_color + ', ' + y.name
                return prod_color

            if attrib == "hs_code":
                hscode = ' '
                for x in temple_records:
                    hscode = x.product_id.hs_code
                return hscode

            if attrib == "qty":
                prod_qty = 0
                for x in temple_records:
                    if x.product_id.product_tmpl_id == current_prod:
                        prod_qty = prod_qty + x.quantity
                return int(prod_qty)

            if attrib == "avg_price":
                avg_price = 0
                total_price = 0
                list_size = len(temple_records)
                for x in temple_records:
                    total_price = total_price + x.price_unit
                avg_price = total_price/list_size
                return int(avg_price)

            if attrib == "total_price":
                total_price = 0
                for x in temple_records:
                    total_price = total_price + x.price_subtotal
                return total_price

            if attrib == "descrip":
                description = 0
                for x in temple_records:
                    description = x.product_id.hs_code
                return description

        sizing_ids = []
        size_list = []

        def set_sizing(prod_id):
            del sizing_ids[:]
            del size_list[:]
            for x in records.invoice_line_ids:
                    if x.product_id.product_tmpl_id == prod_id:
                        sizing_ids.append(x)

            prod_color = ' '
            for x in sizing_ids:
                for y in x.product_id.attribute_value_ids:
                    if y.attribute_id.name == "size":
                        if prod_color == ' ':
                            size_list.append(y.name)
                            prod_color = y.name
                        else:
                            if y.name not in size_list:
                                size_list.append(y.name)
                                prod_color = prod_color + ', ' + y.name

        active_ids = []
        def get_size_qty(sizer,prod_id):
            del active_ids[:]
            for x in records.invoice_line_ids:
                    if x.product_id.product_tmpl_id == prod_id:
                        active_ids.append(x)

            item_qty = 0

            for x in active_ids:
                for y in x.product_id.attribute_value_ids:
                    if y.name == sizer:
                        item_qty = item_qty + x.quantity

            return int(item_qty)

        docargs = {
            'doc_ids': docids,
            'doc_model': 'account.invoice',
            'docs': records,
            'data': data,
            'country': country,
            'temple_ids': temple_ids,
            'temple_products': temple_products,
            'set_sizing': set_sizing,
            'sizing_ids': size_list,
            'get_size_qty': get_size_qty
            }

        return report_obj.render('commercial_invoice_v4.module_report', docargs)

##################### to install num2words ################################
##################### pip install num2words ################################

class Num2Words(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def convert_amount(self):
        word = num2words(self.amount_total)
        word = word.title() + " " + "Only"
        return word