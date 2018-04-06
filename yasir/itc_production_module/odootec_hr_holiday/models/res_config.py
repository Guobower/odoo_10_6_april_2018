# -*- coding: utf-8 -*-
# 
# OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 OdooTec (<http://odootec.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#

from openerp import models, fields, api, SUPERUSER_ID, _


class addsol_hr_attendance_payroll_config_settings(models.TransientModel):
    _inherit = 'hr.config.settings'

    allocation_range = fields.Selection([('month', 'Month'), ('year', 'Year')],
                                        'Allocate automatic leaves every', required=True,
                                        help="Periodicity on which you want automatic allocation of leaves to eligible employees.")

    # def get_default_allocation(self, cr, uid, fields, context=None):
    #     ir_values = self.pool.get('ir.values')
    #     allocation_range = ir_values.get_default(cr, uid, 'hr.config.settings', 'allocation_range')
    #     return {
    #         'allocation_range': allocation_range,
    #     }

    # def set_default_allocation(self, cr, uid, ids, context=None):
    #     ir_values = self.pool.get('ir.values')
    #     wizard = self.browse(cr, uid, ids)[0]
    #     if wizard.allocation_range:
    #         allocation_range = wizard.allocation_range
    #     else:
    #         allocation_range = False
    #     ir_values.set_default(cr, SUPERUSER_ID, 'hr.config.settings', 'allocation_range', allocation_range)

