from odoo import models, fields, api
from datetime import datetime, timedelta
from openerp.tools.translate import _


class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    @api.multi
    def onchange_employee_id(self, date_from, date_to, employee_id=False, contract_id=False):
        res = super(HrPayslip, self).onchange_employee_id(date_from, date_to, employee_id=employee_id,
                                                          contract_id=contract_id)
        contract = self.env['hr.contract'].browse(contract_id)
        day_from = datetime.strptime(date_from, "%Y-%m-%d")
        day_to = datetime.strptime(date_to, "%Y-%m-%d")
        month_days = (day_to - day_from).days + 1
        problem_in_sign_in = 0
        problem_in_sign_in_hours = 0
        absence = 0
        absence_hours = 0
        delays_in = 0
        delays_in_hours = 0
        delays_out = 0
        delays_out_hours = 0

        def employee_holiday(employee_id, datetime_day):
            res = False
            day = datetime_day.strftime("%Y-%m-%d")
            holiday_ids = self.env['hr.holidays'].search([('state', '=', 'validate'),
                                                          ('employee_id', '=', employee_id),
                                                          ('type', '=', 'remove'),
                                                          ('date_from', '<=', day),
                                                          ('date_to', '>=', day)])
            if holiday_ids:
                res = holiday_ids[
                    0].holiday_status_id.name
            return res

        for day in range(0, month_days):
            working_hours_on_day = self.env['resource.calendar'].working_hours_on_day(contract.working_hours,
                                                                                      day_from + timedelta(
                                                                                          days=day))
            leave_type = employee_holiday(employee_id, day_from + timedelta(days=day))
            if leave_type:
                pass
            else:
                attendance_ids = self.env['cleaned.attendance'].search(
                    [('employee_id', '=', employee_id),
                     ('date', '>=', str(datetime.strftime((day_from + timedelta(days=day)).date(), '%Y-%m-%d'))),
                     ('date', '<', str(datetime.strftime((day_from + timedelta(days=day + 1)).date(), '%Y-%m-%d')))])

                if len(attendance_ids) > 0 and working_hours_on_day:
                    first_in = attendance_ids[0].first_in
                    if first_in:
                        intervals_in = contract.working_hours.get_working_intervals_of_day(
                            start_dt=day_from + timedelta(days=day))
                        if intervals_in:
                            if intervals_in[0]:
                                work_from = self.env['resource.calendar'].interval_clean(intervals_in[0])[0][0]
                                attend_date = datetime.strptime(first_in, '%Y-%m-%d %H:%M:%S')
                                mins1 = (attend_date - work_from).seconds % 3600 / 60.0
                                hours1 = (attend_date - work_from).seconds // 3600
                                days1 = (attend_date - work_from).days * 24 * 60
                                total_mins1 = mins1 + (hours1 * 60) + days1
                                rule_apply1 = self.env['delay.rules'].search(
                                    [('structure_id', '=', contract.delay_struct_id.id),
                                     ('delay_period_from', '<=', total_mins1),
                                     ('delay_period_to', '>=', total_mins1)])
                                if total_mins1 > 0:
                                    delays_in += 1
                                    if rule_apply1:
                                        totalnew_1 = rule_apply1.exempted_minutes
                                    else:
                                        totalnew_1 = total_mins1
                                    delays_in_hours += totalnew_1 / 60

                    last_out = attendance_ids[-1].last_out
                    if last_out:
                        intervals_out = contract.working_hours.get_working_intervals_of_day(
                            start_dt=day_from + timedelta(days=day))
                        if intervals_out:
                            if intervals_out[0]:
                                work_to = self.env['resource.calendar'].interval_clean(intervals_out[0])[0][1]

                                leave_date = datetime.strptime(last_out,
                                                               '%Y-%m-%d %H:%M:%S')
                                mins2 = (work_to - leave_date).seconds % 3600 / 60.0
                                hours2 = (work_to - leave_date).seconds // 3600
                                days2 = (work_to - leave_date).days * 24 * 60
                                total_mins2 = mins2 + (hours2 * 60) + days2
                                rule_apply2 = self.env['delay.rules'].search(
                                    [('structure_id', '=', contract.delay_struct_id.id),
                                     ('delay_period_from', '<=', total_mins2),
                                     ('delay_period_to', '>=', total_mins2)])
                                if total_mins2 > 0:
                                    delays_out += 1
                                    if rule_apply2:
                                        totalnew_2 = rule_apply2.exempted_minutes
                                    else:
                                        totalnew_2 = total_mins2
                                    delays_out_hours += totalnew_2 / 60
                    for record in attendance_ids:
                        if record.problem:
                            problem_in_sign_in += 1
                            problem_in_sign_in_hours += contract.delay_struct_id.no_sign_in_out_rate
                if len(attendance_ids) == 0 and working_hours_on_day:
                    absence += 1
                    absence_hours += contract.delay_struct_id.absence_rate * working_hours_on_day

        list_of_inputs = [{
            'name': _("Problem With Sign in or Sign out"),
            'sequence': 3,
            'code': 'no_sign_in',
            'number_of_days': problem_in_sign_in,
            'number_of_hours': problem_in_sign_in_hours,
            'contract_id': contract.id,
        },
            {
                'name': _("Absence"),
                'sequence': 5,
                'code': 'absence',
                'number_of_days': absence,
                'number_of_hours': absence_hours,
                'contract_id': contract.id,
            },
            {
                'name': _("Delay In hours"),
                'sequence': 6,
                'code': 'delay_in',
                'number_of_days': delays_in,
                'number_of_hours': delays_in_hours,
                'contract_id': contract.id,
            },
            {
                'name': _("Delay Out hours"),
                'sequence': 7,
                'code': 'delay_out',
                'number_of_days': delays_out,
                'number_of_hours': delays_out_hours,
                'contract_id': contract.id,
            }
        ]
        if res.get('value'):
            values = res.get('value')
            if values.get('worked_days_line_ids'):
                for item in list_of_inputs:
                    res['value']['worked_days_line_ids'].append(item)

        return res


HrPayslip()
