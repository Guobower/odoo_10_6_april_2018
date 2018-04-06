# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import Warning
from openerp.exceptions import ValidationError
from openerp.exceptions import Warning, ValidationError, UserError
import datetime
from datetime import date, datetime, timedelta
import time
import calendar

class ActualAttendence(models.Model):
	_name = 'actual.attendence'
	_rec_name = 'employee_id'
	
	employee_id = fields.Many2one('hr.employee', string="Employee", required="True")
	department = fields.Many2one('hr.department', string="Department")
	
	checkin = fields.Float(string="Check In")
	checkout = fields.Float(string="Check Out")
	total_time = fields.Float(string="Total Time")
	shift = fields.Char(string="Effective Shift for the day")
	
	intime = fields.Selection([
		('lin', 'Late In'),
		('ein', 'Early In'),
		('-', ' - '),
		],default='-', string="In Time")
	
	outtime = fields.Selection([
		('lout', 'Late Out'),
		('eout', 'Early Out'),
		('-', ' - '),
		],default='-', string="Out Time")
	
	todaystatus = fields.Selection([
		('present', 'Present'),
		('absent', 'Absent'),
		('leave', 'Leave'),
		('holiday', 'Holiday'),
		], string="Status Today")

	non_validate = fields.Boolean(string="Non Validated")
	
	date = fields.Date(string="Date", required="True")

	raw_tree = fields.One2many('ecube.raw.attendance', 'tree_link')

	@api.onchange('employee_id')
	def _get_depart(self):
		self.department = self.employee_id.department_id.id

	@api.multi
	def re_validate(self):

		employees = self.env['hr.employee'].search([])

		for employee in employees:

			attendence = self.env['ecube.raw.attendance'].search([('employee_id.id','=',employee.id),('date','=',self.date)])

			if attendence:

				schedule = employee.schedule
				lavi_time = float(1)

				now = datetime.strptime(self.date, "%Y-%m-%d")
				day = calendar.day_name[now.weekday()]
				in_time = 0
				out_time = 0

				if schedule:
					in_time = float(schedule.intime)
					out_time = float(schedule.outtime)

					sced_in = in_time
					sced_out = out_time

					if in_time < 1:
						in_time = (12 + in_time) - lavi_time
					else:
						in_time = in_time - lavi_time

					out_time = out_time + lavi_time

					total_required = out_time - in_time

					if in_time != 0 or out_time != 0:

						result = '{0:02.0f}:{1:02.0f}'.format(*divmod(in_time * 60, 60))
						intime = datetime.strptime(result, "%H:%M")
						intime_hrs = self.getHours(intime)

						result = '{0:02.0f}:{1:02.0f}'.format(*divmod(out_time * 60, 60))
						outtime = datetime.strptime(result,  "%H:%M")
						outtime_hrs = self.getHours(outtime)

						times = []
						for x in attendence:
							times.append(x.attendance_date)

						final_checkin = 0
						final_checkout = 0
						final_total = 0
						send_vals_in = 0
						send_vals_out = 0

						booleans = False
						newin =  0
						for x in times:
							if self.getHours(x) > intime_hrs and self.getHours(x) < outtime_hrs:
								newin = self.timeToFloat(x)
								final_checkin = newin
								if (final_checkin + 0.25) < sced_in:
									send_vals_in = 1
								elif final_checkin > (sced_in + 0.25):
									send_vals_in = 2
								break

						newout =  0
						for x in reversed(times):
							if self.getHours(x) > intime_hrs and self.getHours(x) < outtime_hrs:
								newout = self.timeToFloat(x)
								break

						if newout != newin:
							final_checkout = newout
							if final_checkout != 0:
								final_total = final_checkout - final_checkin
							else:
								booleans = True
							if (final_checkout + 0.25) < sced_out:
								send_vals_out = 1
							elif final_checkout > (sced_out + 0.25):
								send_vals_out = 2
								
						else:
							booleans = True
							final_checkout = 0
							final_total = 0

						self.checkin = final_checkin
						self.checkout = final_checkout
						self.total_time = final_total

	def getHours(self, date):
		if date:
			raw_date = str(date).split(" ")
			required_date = raw_date[1].split(":")
			new_date = required_date[0]+":"+required_date[1]
			return new_date

	def timeToFloat(self, date):
		if date:
			raw_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
			hours_added_date = raw_date
			diff_in_time = hours_added_date - datetime.strptime(str(hours_added_date.date())+" "+"00:00:00",  "%Y-%m-%d %H:%M:%S") 
			final_hrs = diff_in_time.seconds/3600.0
			return final_hrs

class ActualAttendenceTree(models.Model):
	_inherit = 'ecube.raw.attendance'

	tree_link = fields.Many2one('actual.attendence',string="Tree Link")

class ActualAttendenceWizard(models.Model):
	_name = 'actual.attendence.wizard'

	date = fields.Date(string="Date")

	@api.multi
	def attend_get(self):

		employees = self.env['hr.employee'].search([])

		for employee in employees:

			attendence = self.env['ecube.raw.attendance'].search([('employee_id.id','=',employee.id),('date','=',self.date)])

			if attendence:

				changed = 0
				changed_shift = self.env['change.shift'].search([('form','<=',self.date),('to','>=',self.date)])
				if changed_shift:
					for x in changed_shift:
						for y in x.tree:
							if y.employee_id.id == employee.id:
								schedule = y.shift
								changed = changed + 1
								lavi_time = float(x.lavi)

				if changed == 0:
					schedule = employee.schedule
					lavi_time = float(1)

				now = datetime.strptime(self.date, "%Y-%m-%d")
				day = calendar.day_name[now.weekday()]
				in_time = 0
				out_time = 0

				if schedule:
					in_time = float(schedule.intime)
					out_time = float(schedule.outtime)

					sced_in = in_time
					sced_out = out_time

					if in_time < 1:
						in_time = (12 + in_time) - lavi_time
					else:
						in_time = in_time - lavi_time

					out_time = out_time + lavi_time

					total_required = out_time - in_time

					if in_time != 0 or out_time != 0:

						result = '{0:02.0f}:{1:02.0f}'.format(*divmod(in_time * 60, 60))
						intime = datetime.strptime(result, "%H:%M")
						intime_hrs = self.getHours(intime)

						result = '{0:02.0f}:{1:02.0f}'.format(*divmod(out_time * 60, 60))
						outtime = datetime.strptime(result,  "%H:%M")
						outtime_hrs = self.getHours(outtime)

						times = []
						for x in attendence:
							times.append(x.attendance_date)

						final_checkin = 0
						final_checkout = 0
						final_total = 0

						booleans = False
						newin =  0
						send_vals_in = 0
						send_vals_out = 0

						for x in times:
							if self.getHours(x) > intime_hrs and self.getHours(x) < outtime_hrs:
								newin = self.timeToFloat(x)
								final_checkin = newin
								if (final_checkin + 0.25) < sced_in:
									send_vals_in = 1
								elif final_checkin > (sced_in + 0.25):
									send_vals_in = 2
								break

						newout =  0
						for x in reversed(times):
							if self.getHours(x) > intime_hrs and self.getHours(x) < outtime_hrs:
								newout = self.timeToFloat(x)
								break

						if newout != newin:
							final_checkout = newout
							if final_checkout != 0:
								final_total = final_checkout - final_checkin
							else:
								booleans = True
							if (final_checkout + 0.25) < sced_out:
								send_vals_out = 1
							elif final_checkout > (sced_out + 0.25):
								send_vals_out = 2
								
						else:
							booleans = True
							final_checkout = 0
							final_total = 0
						status = 'present'
						self.MakeRecords(employee,status,final_checkin,final_checkout,final_total,booleans,schedule,send_vals_in,send_vals_out,attendence)

			else:
				year = float(time.strftime('%Y',time.strptime(self.date,'%Y-%m-%d')))
				rec = self.env['holidays.attendence'].search([('year','=',year)])
				leave = self.env['hr.holidays'].search([('employee_id','=',employee.id),('date_from','<=',self.date),('date_to','>=',self.date)])
				counter_strike = 0
				if rec:
					for x in rec.tree:
						if x.date == self.date:
							status = 'holiday'
							counter_strike = counter_strike + 1
							self.MakeRecords(employee,status,final_checkin=False,final_checkout=False,final_total=False,booleans=False,schedule=False,send_vals_in=False,send_vals_out=False,attendence=False)
				
				if counter_strike == 0:
					if leave:
						status = 'leave'
						self.MakeRecords(employee,status,final_checkin=False,final_checkout=False,final_total=False,booleans=False,schedule=False,send_vals_in=False,send_vals_out=False,attendence=False)
				
					else:
						status = 'absent'
						self.MakeRecords(employee,status,final_checkin=False,final_checkout=False,final_total=False,booleans=False,schedule=False,send_vals_in=False,send_vals_out=False,attendence=False)

	def getHours(self, date):
		if date:
			raw_date = str(date).split(" ")
			required_date = raw_date[1].split(":")
			new_date = required_date[0]+":"+required_date[1]
			return new_date

	def timeToFloat(self, date):
		if date:
			raw_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
			hours_added_date = raw_date
			diff_in_time = hours_added_date - datetime.strptime(str(hours_added_date.date())+" "+"00:00:00",  "%Y-%m-%d %H:%M:%S") 
			final_hrs = diff_in_time.seconds/3600.0
			return final_hrs

	def MakeRecords(self,employee,status,final_checkin,final_checkout,final_total,booleans,schedule,send_vals_in,send_vals_out,attendence):

		recorded = self.env['actual.attendence'].search([('employee_id.id','=',employee.id),('date','=',self.date)])
		if recorded:
			recorded.employee_id = employee.id
			recorded.department = employee.department_id.id
			recorded.checkin = final_checkin
			recorded.checkout = final_checkout
			recorded.total_time = final_total
			recorded.date = self.date
			recorded.non_validate = booleans
			if schedule:
				recorded.shift = schedule.name
			recorded.todaystatus = status

			if send_vals_in != 0:
				if send_vals_in == 1:
					recorded.intime = 'ein'
				if send_vals_in == 2:
					recorded.intime = 'lin'

			if send_vals_out != 0:
				if send_vals_out == 1:
					recorded.outtime = 'eout'
				if send_vals_out == 2:
					recorded.outtime = 'lout'

			if attendence:
				for attend in attendence:
					attend.tree_link = recorded.id
					attend.attendence_done = booleans

		else:
			create_order = self.env['actual.attendence'].create({
				'employee_id': employee.id,
				'department': employee.department_id.id,
				'checkin': final_checkin,
				'checkout': final_checkout,
				'total_time': final_total,
				'date': self.date,
				'non_validate': booleans,
				'todaystatus': status
			})
			if schedule:
				create_order.shift = schedule.name

			if send_vals_in != 0:
				if send_vals_in == 1:
					create_order.intime = 'ein'
				if send_vals_in == 2:
					create_order.intime = 'lin'

			if send_vals_out != 0:
				if send_vals_out == 1:
					create_order.outtime = 'eout'
				if send_vals_out == 2:
					create_order.outtime = 'lout'

			if attendence:
				for attend in attendence:
					attend.tree_link = create_order.id
					attend.attendence_done = booleans

class AttendenceShifts(models.Model):
	_name = 'shifts.attendence'
	_rec_name = 'name'

	intime = fields.Float(string="In Time")
	outtime = fields.Float(String="Out Time")
	name = fields.Char(string="Shift")
	main = fields.Boolean(string="Main")

	@api.onchange('intime','outtime')
	def _onchange_times(self):
		intime = self._FloattoTime(self.intime)
		outtime = self._FloattoTime(self.outtime)

		self.name = '%s - %s' %(intime,outtime)


	def _FloattoTime(self, floatTime):
		intime = '{0:02.0f}:{1:02.0f}'.format(*divmod(floatTime*60,60))
		intime_01 = datetime.strptime(intime, "%H:%M")
		intime_02 = str(intime_01).replace(':', ' ', 2)
		intime_03 = intime_02.split(" ")
		intime_04 = '%s:%s' %(intime_03[1],intime_03[2])
		return intime_04

class AttendenceHolidays(models.Model):
	_name = 'holidays.attendence'
	_rec_name = 'year'

	year = fields.Integer(string="Year")
	tree = fields.One2many("holidays.tree","tree_link")

	@api.multi
	def get_sundays(self):
		year = self.year
		items = []
		for x in self.tree:
			items.append(x.date)
		for d in self.allsundays(year):
			if d not in items:
				create_holiday = self.env['holidays.tree'].create({
					'date' : d,
					'day' : 'Sunday',
					'remarks' : 'Sunday Holiday',
					'tree_link' : self.id
				})

	def allsundays(self,attr):
		year = attr
		d = date(year, 1, 1)
		d += timedelta(days = 6 - d.weekday())
		while d.year == year:
			yield d
			d += timedelta(days = 7)

	@api.model
	def create(self, vals):
		new_record = super(AttendenceHolidays, self).create(vals)

		rec = self.env['holidays.attendence'].search([('year','=',new_record.year)])

		if rec:
			raise ValidationError('Cannot Create Two Records Against One Year.')

		else:
			return new_record

class AttendenceHolidaysTree(models.Model):
	_name = 'holidays.tree'
	_rec_name = 'day'

	date = fields.Date(string="Date")
	day = fields.Char(string="Day")
	remarks = fields.Char(string="Remarks")
	tree_link = fields.Char("holidays.attendence")

	@api.onchange('date')
	def _onchange_times(self):
		if self.date:
			now = datetime.strptime(self.date, "%Y-%m-%d")
			self.day = calendar.day_name[now.weekday()]

class ChangeShift(models.Model):
	_name = 'change.shift'
	_rec_name = 'name'

	to = fields.Date(string="To")
	form = fields.Date(string="From")
	name = fields.Char(string="New Shift")
	lavi = fields.Float(string="Lavi")

	tree = fields.One2many("change.shift.tree","tree_link")

	@api.onchange('to','form')
	def _onchange_times(self):
		if self.to or self.form:
			self.name = "%s - %s" %(self.form,self.to)

class ChangeShiftTree(models.Model):
	_name = 'change.shift.tree'
	_rec_name = 'employee_id'

	employee_id = fields.Many2one("hr.employee",string="Employee")
	shift = fields.Many2one('shifts.attendence',string="New Shift")
	remarks = fields.Char(string="Remarks")
	tree_link = fields.Char("change.shift")