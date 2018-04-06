from openerp import models, api
from calendar import monthrange
import datetime


class CleanDummy(models.TransientModel):
    _name = 'clean.dummy.wiz'

    @api.multi
    def clean_dummy(self):
        def get_datetime_range(year, month):
            nb_days = monthrange(year, month)[1]
            return [datetime.datetime(year, month, day, 00, 00, 00) for day in range(1, nb_days + 1)]

        current_month = get_datetime_range(datetime.datetime.now().year, datetime.datetime.now().month)
        print current_month
        for record in current_month:

            for employee_id in self.env['hr.employee'].search([])._ids:

                current_date_attendance = self.env['dummy.attendance'].search(
                    [('date', '>=', str(datetime.datetime.strptime(str(record), '%Y-%m-%d %H:%M:%S'))),
                     ('date', '<', str(datetime.datetime.strftime((record + datetime.timedelta(days=1)),
                                                                  '%Y-%m-%d %H:%M:%S'))),
                     ('employee_id', '=', employee_id), ('cleaned', '=', False)])

                if current_date_attendance:
                    employee_contracts = self.env['hr.contract'].sudo().search([('employee_id', '=', employee_id)])
                    if employee_contracts:
                        for contract in employee_contracts:
                            working_hours_on_day = self.env['resource.calendar'].working_hours_on_day(
                                contract.working_hours,
                                datetime.datetime.strptime(str(record), '%Y-%m-%d %H:%M:%S'))
                            if working_hours_on_day > 0:
                                if len(current_date_attendance) % 2 == 0:
                                    for i in range(0, len(current_date_attendance), 2):
                                        self.env['cleaned.attendance'].create({
                                            'employee_id': employee_id,
                                            'date': str(record.date()),
                                            'first_in': current_date_attendance[i].date,
                                            'last_out': current_date_attendance[i + 1].date
                                        })
                                        current_date_attendance[i].write({'cleaned': True})
                                        current_date_attendance[i + 1].write({'cleaned': True})
                                else:

                                    for i in range(0, len(current_date_attendance) - 1, 2):
                                        self.env['cleaned.attendance'].create({
                                            'employee_id': employee_id,
                                            'date': str(record.date()),
                                            'first_in': current_date_attendance[i].date,
                                            'last_out': current_date_attendance[i + 1].date
                                        })
                                        current_date_attendance[i].write({'cleaned': True})
                                        current_date_attendance[i + 1].write({'cleaned': True})
                                    intervals_in = contract.working_hours.get_working_intervals_of_day(
                                        start_dt=record)
                                    if intervals_in:
                                        if intervals_in[0]:
                                            work_from = \
                                                self.env['resource.calendar'].interval_clean(intervals_in[0])[0][0]
                                            work_to = \
                                                self.env['resource.calendar'].interval_clean(intervals_in[0])[0][
                                                    1]
                                        if work_from and work_to:
                                            work1 = datetime.datetime.strptime(current_date_attendance[-1].date,
                                                                               '%Y-%m-%d %H:%M:%S') - work_from
                                            work2 = work_to - datetime.datetime.strptime(
                                                current_date_attendance[-1].date,
                                                '%Y-%m-%d %H:%M:%S')
                                            if work2 > work1:
                                                note = "I think it's sign in"
                                                action = 'in'
                                            else:
                                                note = "I think it's sign out"
                                                action = 'out'
                                    if self.env['to.clean.attendance'].search([('employee_id', '=', employee_id), (
                                            'date', '=',
                                            str(datetime.datetime.strptime(current_date_attendance[-1].date,
                                                                           '%Y-%m-%d %H:%M:%S').date()))]):
                                        self.env['to.clean.attendance'].search([('employee_id', '=', employee_id), (
                                            'date', '=',
                                            str(datetime.datetime.strptime(current_date_attendance[-1].date,
                                                                           '%Y-%m-%d %H:%M:%S').date()))]).sudo().unlink()
                                    self.env['to.clean.attendance'].create({
                                        'employee_id': employee_id,
                                        'date': str(datetime.datetime.strptime(current_date_attendance[-1].date,
                                                                               '%Y-%m-%d %H:%M:%S').date()),
                                        'attendance_line_ids': [
                                            (0, 0, {
                                                'date': str(
                                                    datetime.datetime.strptime(current_date_attendance[-1].date,
                                                                               '%Y-%m-%d %H:%M:%S')),
                                                'dummy_id': current_date_attendance[-1].id,
                                                'note': note,
                                                'action': action,
                                            })],
                                        'state': 'to_approve',
                                    })


CleanDummy()
