#-*- coding:utf-8 -*-
from datetime import datetime, timedelta , date
from dateutil.relativedelta import relativedelta
import time
from odoo import models, fields, api


class MyDash(models.Model):
	_name = 'my.dash'
	_rec_name = 'name'
	_description = 'New Description'

	current_member_count = fields.Integer(string="Current Members Gulberg", compute='count_current_members')
	current_member_count_gulberg = fields.Integer(string="Current Members Gulberg", compute='count_current_members_gulberg')
	current_member_count_dha = fields.Integer(string="Current Members Dha Lahore", compute='count_current_members_dha')
	current_member_count_jt = fields.Integer(string="Current Members Dha Johar Town", compute='count_current_members_jt')
	current_member_count_kchi = fields.Integer(string="Current Members Dha Karachi", compute='count_current_members_kchi')
	new_members_count = fields.Integer(string="Cancel Members", compute='new_members')
	new_members_count_gulberg = fields.Integer(string="Cancel Members", compute='new_members_gulberg')
	new_members_count_dha = fields.Integer(string="Cancel Members", compute='new_members_dha')
	new_members_count_jt = fields.Integer(string="Cancel Members", compute='new_members_jt')
	new_members_count_kchi = fields.Integer(string="Cancel Members", compute='new_members_kchi')
	cancel_member_count = fields.Integer(string="Cancel Members", compute='count_cancel_members')
	cancel_member_count_gulberg = fields.Integer(string="Cancel Members", compute='count_cancel_members_gulberg')
	cancel_member_count_dha = fields.Integer(string="Cancel Members", compute='count_cancel_members_dha')
	cancel_member_count_jt = fields.Integer(string="Cancel Members", compute='count_cancel_members_jt')
	cancel_member_count_kchi = fields.Integer(string="Cancel Members", compute='count_cancel_members_kchi')
	cancel_massage_count = fields.Integer(string="Cancel Massage", compute='count_cancel_massage')
	cancel_massage_count_gulberg = fields.Integer(string="Cancel Massage", compute='count_cancel_massage_gulberg')
	cancel_massage_count_dha = fields.Integer(string="Cancel Massage", compute='count_cancel_massage_dha')
	cancel_massage_count_jt = fields.Integer(string="Cancel Massage", compute='count_cancel_massage_jt')
	cancel_massage_count_kchi = fields.Integer(string="Cancel Massage", compute='count_cancel_massage_kchi')
	booked_massage_count = fields.Integer(string="Cancel Massage", compute='count_booked_massage')
	booked_massage_count_gulberg = fields.Integer(string="Cancel Massage", compute='count_booked_massage_gulberg')
	booked_massage_count_dha = fields.Integer(string="Cancel Massage", compute='count_booked_massage_dha')
	booked_massage_count_jt = fields.Integer(string="Cancel Massage", compute='count_booked_massage_jt')
	booked_massage_count_kchi = fields.Integer(string="Cancel Massage", compute='count_booked_massage_kchi')
	daily_visitor_count = fields.Integer(string="Daily Visitor", compute='count_daily_visitor')
	daily_visitor_count_gulberg = fields.Integer(string="Daily Visitor", compute='count_daily_visitor_gulberg')
	daily_visitor_count_dha = fields.Integer(string="Daily Visitor", compute='count_daily_visitor_dha')
	daily_visitor_count_jt = fields.Integer(string="Daily Visitor", compute='count_daily_visitor_jt')
	daily_visitor_count_kchi = fields.Integer(string="Daily Visitor", compute='count_daily_visitor_kchi')
	monthly_visitor_count = fields.Integer(string="Daily Visitor", compute='count_monthly_visitor')
	monthly_visitor_count_gulberg = fields.Integer(string="Daily Visitor", compute='count_monthly_visitor_gulberg')
	monthly_visitor_count_dha = fields.Integer(string="Daily Visitor", compute='count_monthly_visitor_dha')
	monthly_visitor_count_jt = fields.Integer(string="Daily Visitor", compute='count_monthly_visitor_jt')
	monthly_visitor_count_kchi = fields.Integer(string="Daily Visitor", compute='count_monthly_visitor_kchi')
	daily_receipts_amount = fields.Integer(string="Daily Receipts Amount", compute='_daily_receipts_amount')
	daily_receipts_amount_gulberg = fields.Integer(string="Daily Receipts Amount", compute='_daily_receipts_amount_gulberg')
	daily_receipts_amount_dha = fields.Integer(string="Daily Receipts Amount", compute='_daily_receipts_amount_dha')
	daily_receipts_amount_jt = fields.Integer(string="Daily Receipts Amount", compute='_daily_receipts_amount_jt')
	daily_receipts_amount_kchi = fields.Integer(string="Daily Receipts Amount", compute='_daily_receipts_amount_kchi')
	monthly_receipts_amount = fields.Integer(string="Monthly Receipts Amount", compute='_monthly_receipts_amount')
	monthly_receipts_amount_gulberg = fields.Integer(string="Monthly Receipts Amount", compute='_monthly_receipts_amount_gulberg')
	monthly_receipts_amount_dha = fields.Integer(string="Monthly Receipts Amount", compute='_monthly_receipts_amount_dha')
	monthly_receipts_amount_jt = fields.Integer(string="Monthly Receipts Amount", compute='_monthly_receipts_amount_jt')
	monthly_receipts_amount_kchi = fields.Integer(string="Monthly Receipts Amount", compute='_monthly_receipts_amount_kchi')
	name = fields.Char()

	def create_my_dash(self):
		record = self.env['my.dash'].create({
			'name':"My DashBoard"
		})


	@api.one
	def count_current_members(self):
		self.current_member_count = self.env['reg.form'].search_count([('stages', '=', 'member')])

	@api.one
	def count_current_members_gulberg(self):
		self.current_member_count_gulberg = self.env['reg.form'].search_count([('stages', '=', 'member'),('branch','=',1)])

	@api.one
	def count_current_members_dha(self):
		self.current_member_count_dha = self.env['reg.form'].search_count([('stages', '=', 'member'),('branch','=',2)])

	@api.one
	def count_current_members_jt(self):
		self.current_member_count_jt = self.env['reg.form'].search_count([('stages', '=', 'member'),('branch','=',3)])

	@api.one
	def count_current_members_kchi(self):
		self.current_member_count_kchi = self.env['reg.form'].search_count([('stages', '=', 'member'),('branch','=',4)])

	@api.one
	def new_members(self):
		current_month = str(date.today())
		rec = self.env['reg.form'].search([('stages', '=', 'member')])
		count = 0
		for x in rec:
			if x.joining:
				if str(x.joining[:7]) == str(current_month[:7]):
					count = count + 1
		self.new_members_count = count

	@api.one
	def new_members_gulberg(self):
		current_month = str(date.today())
		rec = self.env['reg.form'].search([('stages', '=', 'member'),('branch','=',1)])
		count = 0
		for x in rec:
			if x.joining:
				if str(x.joining[:7]) == str(current_month[:7]):
					count = count + 1
		self.new_members_count_gulberg = count


	@api.one
	def new_members_dha(self):
		current_month = str(date.today())
		rec = self.env['reg.form'].search([('stages', '=', 'member'),('branch','=',2)])
		count = 0
		for x in rec:
			if x.joining:
				if str(x.joining[:7]) == str(current_month[:7]):
					count = count + 1
		self.new_members_count_dha = count


	@api.one
	def new_members_jt(self):
		current_month = str(date.today())
		rec = self.env['reg.form'].search([('stages', '=', 'member'),('branch','=',3)])
		count = 0
		for x in rec:
			if x.joining:
				if str(x.joining[:7]) == str(current_month[:7]):
					count = count + 1
		self.new_members_count_jt = count

	@api.one
	def new_members_kchi(self):
		current_month = str(date.today())
		rec = self.env['reg.form'].search([('stages', '=', 'member'),('branch','=',4)])
		count = 0
		for x in rec:
			if x.joining:
				if str(x.joining[:7]) == str(current_month[:7]):
					count = count + 1
		self.new_members_count_kchi = count

	@api.one
	def count_cancel_members(self):
		self.cancel_member_count = self.env['reg.form'].search_count([('stages', '=', 'cancel')])

	@api.one
	def count_cancel_members_gulberg(self):
		self.cancel_member_count_gulberg = self.env['reg.form'].search_count([('stages', '=', 'cancel'),('branch','=',1)])

	@api.one
	def count_cancel_members_dha(self):
		self.cancel_member_count_dha = self.env['reg.form'].search_count([('stages', '=', 'cancel'),('branch','=',2)])

	@api.one
	def count_cancel_members_jt(self):
		self.cancel_member_count_jt = self.env['reg.form'].search_count([('stages', '=', 'cancel'),('branch','=',3)])

	@api.one
	def count_cancel_members_kchi(self):
		self.cancel_member_count_kchi = self.env['reg.form'].search_count([('stages', '=', 'cancel'),('branch','=',4)])

	@api.one
	def count_cancel_massage(self):
		self.cancel_massage_count = self.env['struct.appointment'].search_count([('stages', '=', 'cancel')])

	@api.one
	def count_cancel_massage_gulberg(self):
		self.cancel_massage_count_gulberg = self.env['struct.appointment'].search_count([('stages', '=', 'cancel'),('branch','=',1)])

	@api.one
	def count_cancel_massage_dha(self):
		self.cancel_massage_count_dha = self.env['struct.appointment'].search_count([('stages', '=', 'cancel'),('branch','=',2)])

	@api.one
	def count_cancel_massage_jt(self):
		self.cancel_massage_count_jt = self.env['struct.appointment'].search_count([('stages', '=', 'cancel'),('branch','=',3)])

	@api.one
	def count_cancel_massage_kchi(self):
		self.cancel_massage_count_kchi = self.env['struct.appointment'].search_count([('stages', '=', 'cancel'),('branch','=',4)])

	@api.one
	def count_booked_massage(self):
		self.booked_massage_count = self.env['struct.appointment'].search_count([('stages', '=', 'booked')])

	@api.one
	def count_booked_massage_gulberg(self):
		self.booked_massage_count_gulberg = self.env['struct.appointment'].search_count([('stages', '=', 'booked'),('branch','=',1)])

	@api.one
	def count_booked_massage_dha(self):
		self.booked_massage_count_dha = self.env['struct.appointment'].search_count([('stages', '=', 'booked'),('branch','=',2)])

	@api.one
	def count_booked_massage_jt(self):
		self.booked_massage_count_jt = self.env['struct.appointment'].search_count([('stages', '=', 'booked'),('branch','=',3)])

	@api.one
	def count_booked_massage_kchi(self):
		self.booked_massage_count_kchi = self.env['struct.appointment'].search_count([('stages', '=', 'booked'),('branch','=',4)])

	@api.one
	def count_daily_visitor(self):
		self.daily_visitor_count = self.env['struct.visitor'].search_count([('date','=',date.today())])

	@api.one
	def count_daily_visitor_gulberg(self):
		self.daily_visitor_count_gulberg = self.env['struct.visitor'].search_count([('date','=',date.today()),('branch','=',1)])

	@api.one
	def count_daily_visitor_dha(self):
		self.daily_visitor_count_dha = self.env['struct.visitor'].search_count([('date','=',date.today()),('branch','=',2)])

	@api.one
	def count_daily_visitor_jt(self):
		self.daily_visitor_count_jt = self.env['struct.visitor'].search_count([('date','=',date.today()),('branch','=',3)])

	@api.one
	def count_daily_visitor_kchi(self):
		self.daily_visitor_count_kchi = self.env['struct.visitor'].search_count([('date','=',date.today()),('branch','=',4)])



	@api.one
	def count_monthly_visitor(self):
		current_month = str(date.today())
		rec = self.env['struct.visitor'].search([])
		count = 0
		for x in rec:
			if x.date:
				if str(x.date[:7]) == str(current_month[:7]):
					count = count + 1
		self.monthly_visitor_count = count

	@api.one
	def count_monthly_visitor_gulberg(self):
		current_month = str(date.today())
		rec = self.env['struct.visitor'].search([('branch','=',1)])
		count = 0
		for x in rec:
			if x.date:
				if str(x.date[:7]) == str(current_month[:7]):
					count = count + 1
		self.monthly_visitor_count_gulberg = count

	@api.one
	def count_monthly_visitor_dha(self):
		current_month = str(date.today())
		rec = self.env['struct.visitor'].search([('branch','=',2)])
		count = 0
		for x in rec:
			if x.date:
				if str(x.date[:7]) == str(current_month[:7]):
					count = count + 1
		self.monthly_visitor_count_dha = count

	@api.one
	def count_monthly_visitor_jt(self):
		current_month = str(date.today())
		rec = self.env['struct.visitor'].search([('branch','=',3)])
		count = 0
		for x in rec:
			if x.date:
				if str(x.date[:7]) == str(current_month[:7]):
					count = count + 1
		self.monthly_visitor_count_jt = count

	@api.one
	def count_monthly_visitor_kchi(self):
		current_month = str(date.today())
		rec = self.env['struct.visitor'].search([('branch','=',4)])
		count = 0
		for x in rec:
			if x.date:
				if str(x.date[:7]) == str(current_month[:7]):
					count = count + 1
		self.monthly_visitor_count_kchi = count


	@api.one
	def _daily_receipts_amount(self):
		rec = self.env['customer.payment.bcube'].search([('date', '=', date.today()),('receipts', '=',True)])
		for x in rec:
			self.daily_receipts_amount = self.daily_receipts_amount + x.amount

	@api.one
	def _daily_receipts_amount_gulberg(self):
		rec = self.env['customer.payment.bcube'].search([('date', '=', date.today()),('receipts', '=',True),('branch','=',1)])
		for x in rec:
			self.daily_receipts_amount_gulberg = self.daily_receipts_amount_gulberg + x.amount


	@api.one
	def _daily_receipts_amount_dha(self):
		rec = self.env['customer.payment.bcube'].search([('date', '=', date.today()),('receipts', '=',True),('branch','=',2)])
		for x in rec:
			self.daily_receipts_amount_dha = self.daily_receipts_amount_dha + x.amount


	@api.one
	def _daily_receipts_amount_jt(self):
		rec = self.env['customer.payment.bcube'].search([('date', '=', date.today()),('receipts', '=',True),('branch','=',3)])
		for x in rec:
			self.daily_receipts_amount_jt = self.daily_receipts_amount_jt + x.amount

	@api.one
	def _daily_receipts_amount_kchi(self):
		rec = self.env['customer.payment.bcube'].search([('date', '=', date.today()),('receipts', '=',True),('branch','=',4)])
		for x in rec:
			self.daily_receipts_amount_kchi = self.daily_receipts_amount_kchi + x.amount

	@api.one
	def _monthly_receipts_amount(self):
		current_month = str(date.today())
		rec = self.env['customer.payment.bcube'].search([('receipts', '=', True)])
		for x in rec:
			if str(x.date[:7]) == str(current_month[:7]):
				self.monthly_receipts_amount = self.monthly_receipts_amount + x.amount

	@api.one
	def _monthly_receipts_amount_gulberg(self):
		current_month = str(date.today())
		rec = self.env['customer.payment.bcube'].search([('receipts', '=', True),('branch','=',1)])
		for x in rec:
			if str(x.date[:7]) == str(current_month[:7]):
				self.monthly_receipts_amount_gulberg = self.monthly_receipts_amount_gulberg + x.amount

	@api.one
	def _monthly_receipts_amount_dha(self):
		current_month = str(date.today())
		rec = self.env['customer.payment.bcube'].search([('receipts', '=', True),('branch','=',2)])
		for x in rec:
			if str(x.date[:7]) == str(current_month[:7]):
				self.monthly_receipts_amount_dha = self.monthly_receipts_amount_dha + x.amount

	@api.one
	def _monthly_receipts_amount_jt(self):
		current_month = str(date.today())
		rec = self.env['customer.payment.bcube'].search([('receipts', '=', True),('branch','=',3)])
		for x in rec:
			if str(x.date[:7]) == str(current_month[:7]):
				self.monthly_receipts_amount_jt = self.monthly_receipts_amount_jt + x.amount

	@api.one
	def _monthly_receipts_amount_kchi(self):
		current_month = str(date.today())
		rec = self.env['customer.payment.bcube'].search([('receipts', '=', True),('branch','=',4)])
		for x in rec:
			if str(x.date[:7]) == str(current_month[:7]):
				self.monthly_receipts_amount_kchi = self.monthly_receipts_amount_kchi + x.amount
				