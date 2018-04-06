# -*- coding: utf-8 -*-
# 
#    OpenERP, Open Source Management Solution
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

from openerp import models, fields, api, _


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    @api.model
    def create(self, vals):
        # don't pass the value of paid leave if it's 0 at the creation time, otherwise it will trigger the inverse
        # function _set_remaining_days and the system may not be configured for. Note that we don't have this problem on
        # the write because the clients only send the fields that have been modified.
        if 'unpaid_leaves' in vals and not vals['unpaid_leaves']:
            del(vals['unpaid_leaves'])
        return super(HrEmployee, self).create(vals)

    @api.one
    def _get_paid_leaves(self):
        for record in self:
            self.env.cr.execute("""SELECT
                    sum(h.number_of_days) as days
                from
                    hr_holidays h
                    join hr_holidays_status s on (s.id=h.holiday_status_id)
                where
                    h.state='validate' and h.type ='remove' and
                    s.is_unpaid_leave = True and
                    h.employee_id = %s

                """, (record.id,))
            res = self.env.cr.dictfetchall()
            if res:
                record.unpaid_leaves = res[0].get('days', 0.00) and -res[0].get('days', 0.00)
            else:
                record.unpaid_leaves = 0.0



    unpaid_leaves = fields.Float(string='UnPaid Leaves', compute=_get_paid_leaves,
                               help='Total number of unpaid leaves allocated to this employee')