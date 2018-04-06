from odoo import models, fields, api
from datetime import datetime
from openerp.exceptions import Warning
from openerp.tools.translate import _


class DummyAttendance(models.Model):
    _name = 'dummy.attendance'
    _rec_name = 'employee_id'
    employee_int = fields.Integer(string='Employee ID', required=True)
    date = fields.Datetime(string='Action Date', required=True)
    employee_id = fields.Many2one(comodel_name='hr.employee', compute='_get_employee_id', store=True)
    cleaned = fields.Boolean(string='Cleaned', readonly=True)

#     @api.one
#     @api.depends('employee_int')
#     def _get_employee_id(self):
#         for record in self:
#             if record.employee_int:
#                 employee = self.env['hr.employee'].search([('machine_int', '=', record.employee_int)])
#                 if employee:
#                     record.employee_id = employee.id


# DummyAttendance()


class ToBeCleanedAttendance(models.Model):
    _name = 'to.clean.attendance'
    _rec_name = 'employee_id'
    employee_id = fields.Many2one(comodel_name='hr.employee', required=True, string='Employee')

    date = fields.Date(string='Date')
    attendance_line_ids = fields.One2many(comodel_name='to.clean.attendance.line', inverse_name='line_id',
                                          string='Not Cleaned Lines')
    state = fields.Selection(
        selection=[('draft', 'Draft'), ('to_approve', 'submitted'), ('approved', 'Approved'), ('refuse', 'Refused')],
        string='State', default='draft', required=True)

#     @api.multi
#     def set_state_approved(self):
#         if len(self.attendance_line_ids) % 2 != 0:
#             raise Warning(_("You can't approve these records,it's unmatched.\n"
#                             "Please Check these records again."))
#         else:
#             in_ids = self.attendance_line_ids.filtered(lambda r: r.action == 'in')
#             out_ids = self.attendance_line_ids.filtered(lambda r: r.action == 'out')
#             if len(in_ids) != len(out_ids):
#                 raise Warning(_("You can't approve these records,it's unmatched.\n"
#                                 "Please Check these records again."))
#             else:
#                 for first, last in zip(in_ids._ids, out_ids._ids):
#                     self.env['cleaned.attendance'].create({
#                         'employee_id': self.employee_id.id,
#                         'date': self.date,
#                         'first_in': self.env['to.clean.attendance.line'].browse(first).date,
#                         'last_out': self.env['to.clean.attendance.line'].browse(last).date,
#                         'problem': True
#                     })
#                     if self.env['to.clean.attendance.line'].browse(first).dummy_id:
#                         self.env['to.clean.attendance.line'].browse(first).dummy_id.write(
#                             {'cleaned': True, })
#                     if self.env['to.clean.attendance.line'].browse(last).dummy_id:
#                         self.env['to.clean.attendance.line'].browse(last).dummy_id.write(
#                             {'cleaned': True})
#                 self.write({'state': 'approved'})

#     @api.multi
#     def set_state_draft(self):
#         self.write({'state': 'draft'})

#     @api.multi
#     def set_state_to_approve(self):
#         self.write({'state': 'to_approve'})

#     @api.multi
#     def set_state_refused(self):
#         self.write({'state': 'refuse'})


# ToBeCleanedAttendance()


class ToBeCleanedAttendanceLine(models.Model):
    _name = 'to.clean.attendance.line'
    _rec_name = 'line_id'
    line_id = fields.Many2one(comodel_name='to.clean.attendance', string='Attendance Line')
    dummy_id = fields.Many2one(comodel_name='dummy.attendance', string='Related Dummy', readonly=True)
    date = fields.Datetime(string='Action Datetime')
    note = fields.Char(string='Action Note')
    action = fields.Selection(selection=[('in', 'Sign In'), ('out', 'Sign out')], string='The Clean Action')


# ToBeCleanedAttendanceLine()


class CleanedAttendance(models.Model):
    _name = 'cleaned.attendance'
    _rec_name = 'employee_id'
    employee_id = fields.Many2one(comodel_name='hr.employee', required=True, string='Employee')
    date = fields.Date(string='Work Date')
    first_in = fields.Datetime(string='First Action', required=True)
    last_out = fields.Datetime(string='Last Action', required=True)
    problem = fields.Boolean()
    worked_hours = fields.Float(compute='_get_worked_hours', string='Worked Hours')

#     @api.one
#     @api.depends('first_in', 'last_out')
#     def _get_worked_hours(self):
#         for record in self:
#             if record.first_in and record.last_out:
#                 last_signin_datetime = datetime.strptime(record.first_in, '%Y-%m-%d %H:%M:%S')
#                 signout_datetime = datetime.strptime(record.last_out, '%Y-%m-%d %H:%M:%S')
#                 workedhours_datetime = (signout_datetime - last_signin_datetime)
#                 record.worked_hours = ((workedhours_datetime.seconds) / 60) / 60.0


# CleanedAttendance()
