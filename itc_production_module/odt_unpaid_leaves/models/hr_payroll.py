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

from openerp import models, fields, api, _
from datetime import datetime, timedelta


class SalaryRuleInput(models.Model):
    _inherit = 'hr.payslip'

    @api.model
    def get_inputs(self, contract_ids, date_from, date_to):
        res = super(SalaryRuleInput, self).get_inputs(contract_ids, date_from, date_to)
        contract_obj = self.env['hr.contract']
        unpaid_leaves = 0.0
        for contract in contract_obj.browse(contract_ids):
            self.env.cr.execute("""SELECT
                    sum(h.number_of_days) as days
                from
                    hr_holidays h
                    join hr_holidays_status s on (s.id=h.holiday_status_id)
                where
                    h.state='validate' and h.type ='remove' and
                    s.is_unpaid_leave = True and
                    h.employee_id = %s and h.date_from <= %s and h.date_to >= %s

                """, (contract.employee_id.id, date_to, date_from))
            re = self.env.cr.dictfetchall()
            if re and re[0].get('days'):
                unpaid_leaves += re[0].get('days', 0.00) and -re[0].get('days', 0.00) * contract.unpaid_leave_cost

            # create input lines for unpaid deduction
            for result in res:
                if result.get('code') == 'UNPAID':
                    result['amount'] = unpaid_leaves
        return res


