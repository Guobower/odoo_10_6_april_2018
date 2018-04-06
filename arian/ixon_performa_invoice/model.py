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
from num2words import num2words


class SampleDevelopmentReport(models.AbstractModel):
    _name = 'report.ixon_performa_invoice.module_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('ixon_performa_invoice.module_report')
        records = self.env['sale.order'].browse(docids)

        enteries = []
        for x in records.order_line:
          if x.product_id.product_tmpl_id not in enteries:
               enteries.append(x.product_id.product_tmpl_id)

        def getpieces(item):
            total_qty = 0
            records = self.env['sale.order'].search([('id','=',item.id)])
            for x in records.order_line:
                total_qty = total_qty + x.product_uom_qty

            return int(total_qty)


        sizes = []
        size_names = []
        looped = []
        def sizeing(current_record,attr,count):
            del sizes[:]
            del size_names[:]

            for x in records.order_line:
                if x.product_id.product_tmpl_id == current_record:
                    sizes.append(x)

            for x in sizes:
                for y in x.product_id.attribute_value_ids:
                    if y.attribute_id.name == "size":
                        if y.name not in size_names:
                            size_names.append(y.name)

            counted_class = 0
            for x in size_names:
                counted_class = counted_class + 1

            if attr == 'lefter':
                del looped[:]
                left_size = counted_class - count

                if left_size > 0:
                    for x in range(0, left_size):
                        looped.append(x)

            if counted_class > count:
                if attr == 'name':
                    size_name = size_names[count]
                    return size_name

                if attr == 'qty':
                    varient_list = []
                    size_name = size_names[count]
                    for x in sizes:
                        for y in x.product_id.attribute_value_ids:
                            if y.attribute_id.name == "size":
                                if y.name == size_name:
                                    varient_list.append(x)

                    qty = 0
                    for x in varient_list:
                        qty = qty + x.product_uom_qty

                    return qty

                if attr == 'rate':
                    varient_list = []
                    size_name = size_names[count]
                    for x in sizes:
                        for y in x.product_id.attribute_value_ids:
                            if y.attribute_id.name == "size":
                                if y.name == size_name:
                                    varient_list.append(x)

                    rate = 0
                    for x in varient_list:
                        rate = rate + x.price_unit

                    return rate

                if attr == 'total':
                    varient_list = []
                    size_name = size_names[count]
                    for x in sizes:
                        for y in x.product_id.attribute_value_ids:
                            if y.attribute_id.name == "size":
                                if y.name == size_name:
                                    varient_list.append(x)

                    total = 0
                    for x in varient_list:
                        total = total + x.price_subtotal

                    return total

            else:
                return 0

        varients = []
        def getdata(current_record,attrb):
            del varients[:]
            for x in records.order_line:
                if x.product_id.product_tmpl_id == current_record:
                    varients.append(x)

            if attrb == "style":
                style = ""
                for x in records.order_line:
                    if x.product_id.product_tmpl_id == current_record:
                        style = x.product_id.style_no
                return style

            if attrb == "hs_code":
                hscode = ""
                for x in records.order_line:
                    if x.product_id.product_tmpl_id == current_record:
                        hscode = x.product_id.hs_code
                return hscode

            if attrb == "composition":
                composition = ""
                for x in records.order_line:
                    if x.product_id.product_tmpl_id == current_record:
                        composition = x.product_id.composition
                return composition

            if attrb == "desc":
                desc = ""
                for x in records.order_line:
                    if x.product_id.product_tmpl_id == current_record:
                        desc = x.name
                return desc

            if attrb == "color":
                color = ''
                colors = []
                for x in varients:
                    for y in x.product_id.attribute_value_ids:
                        if y.attribute_id.name == "color":
                            if color == '':
                                colors.append(y.name)
                                color = y.name
                            else:
                                if y.name not in color:
                                    colors.append(y.name)
                                    color = color + " , " + y.name
                return color

        docargs = {
            'doc_ids': docids,
            'doc_model': 'sale.order',
            'docs': records,
            'data': data,
            'entries': enteries,
            'getdata': getdata,
            'sizeing': sizeing,
            'sizes': sizes,
            'size_names': size_names,
            'looped': looped,
            'getpieces': getpieces
        }

        return report_obj.render('ixon_performa_invoice.module_report', docargs)

                ##################### pip install num2words ################################


class Num2Words(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def number_to_words(self):
        word = num2words((self.amount_untaxed))
        word = word.title() + " " + "Only"
        return word