# -*- coding:utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Savoir-faire Linux. All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
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
import pytz
from datetime import datetime, date

from openerp import models, fields, api, _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT


# def get_current_year(context):
#     if not context:
#         context = {}
#     tz = context.get('tz', False)
#     tz = tz and pytz.timezone(tz) or pytz.utc
#     return datetime.now(tz).year


class HolidayAnalysis(models.TransientModel):
    """
    Wizard to generate holiday analysis report
    """
    _name = 'hr.holiday.report.wiz'
    _description = 'Holiday Report Wizard'

    period = fields.Selection(
        [
            ('current_year', 'Current Year'),
            ('previous_year', 'Previous Year'),
            ('every_year', 'Every Year'),
        ],
        string='Analysis Period',
        default='current_year'
    )
    start_date = fields.Datetime(
        'Start Date',
        default=lambda self: (
            date(get_current_year(self.env.context), 1, 1).strftime(
                DEFAULT_SERVER_DATE_FORMAT))
    )
    end_date = fields.Datetime(
        'End Date',
        default=lambda self: (
            date(get_current_year(self.env.context), 12, 31).strftime(
                DEFAULT_SERVER_DATE_FORMAT))
        )

    employee_ids = fields.Many2many(
        'hr.employee',
        'holiday_report_employee_rel',
        'holiday_report_id',
        'employee_id',
        'Employees'
    )


    # @api.onchange('period')
    # @api.one
    # def onchange_period(self):
    #     if self.period:
    #         if self.period == 'every_year':
    #             self.start_date = False
    #             self.end_date = False

    #         year = get_current_year(self.env.context)

    #         if self.period == 'previous_year':
    #             year -= 1

    #         start_date = date(year, 1, 1).strftime(DEFAULT_SERVER_DATE_FORMAT)
    #         end_date = date(year, 12, 31).strftime(DEFAULT_SERVER_DATE_FORMAT)

    #         self.start_date = start_date
    #         self.end_date = end_date

    # def holiday_analysis_open_window(self, cr, uid,ids, context=None):
    #     """
    #     This method returns an action that displays Report
    #     """
    #     if context is None:
    #         context = {}
    #     data = {}
    #     data['ids'] = context.get('active_ids', [])
    #     data['model'] = 'hr.holidays'
    #     data['form'] = self.read(cr, uid, ids, context=context)[0]
    #     return self.pool['report'].get_action(cr, uid, [],
    #                                           'odootec_hr_holiday.hr_holiday_report',
    #                                           data=data,
    #                                           context=context)