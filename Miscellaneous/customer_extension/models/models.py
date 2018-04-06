# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CustomerExtension(models.Model):
	""" MAin FOrm class  """
	_inherit = 'res.partner'

	business_code = fields.Many2one('business.code',string='Business Code')
	plan_name = fields.Many2one('plane.name',string='Plan Name')
	pension_benefit = fields.Many2one('pension.benefit.code',string='Pension Benefit Code')
	customer_month = fields.Selection([('january','January'),('february','February'),('march','March')
		,('april','April'),('may','May')
		,('june','June'),('july','July')
		,('august','August'),('september','September')
		,('october','October'),('november','November'),('december','December')],default='january')
	product_ids	= fields.One2many('res.tree','partent_id')
	plane_score = fields.Char(string='Plan Score')
	number_of_red_flags = fields.Char(string='# of Red Flags')
	partic_total = fields.Char(string='Participants: Total')
	tot_pal_ass = fields.Char(string='Total Plan Assets')
	plan_number = fields.Char(string='Plan Number')
	total_plane_for_ein = fields.Char(string='# of Red Flags')

	sponsor_ein = fields.Char(string='Sponsor EIN')
	plane_number = fields.Char(string='Plane Number')
	plane_name = fields.Char(string='Plane Name')
	splane_renewal = fields.Char(string='Plane Renewal Month (1-12)')
	pen_ben_code = fields.Char(string='Pension Benefit Code(s)')
	acc_firm_name = fields.Char(string='Accountant Firm Name')
	annuitiy_gic_carr_name = fields.Char(string='Annuity/GIC 01: Carrier Name')
	provider_name_01 = fields.Char(string='Provider 01: Provider Name')
	provider_name_02 = fields.Char(string='Provider 02: Provider Name')

	plan_score = fields.Char(string='Plan Score')
	partic_total = fields.Char(string='Participants: Total')
	active_total = fields.Char(string='Participants: Active Total')
	partic_rate = fields.Char(string='Participation Rate')
	# tot_pal_ass = fields.Char(string='Total Plan Assets')
	rat_of_retu = fields.Char(string='Rate of Return (1 year)')
	rat_of_retu_3 = fields.Char(string='Rate of Return Over 3 Years')
	rat_of_retu_5= fields.Char(string='Rate of Return Over 5 Years')
	ave_par_bal = fields.Char(string='Average Participant Balance')
	ave_accou_bal = fields.Char(string='Average Account Balance 1 Year Growth')
	total_contri = fields.Char(string='Total Contributions')
	ave_401_contri = fields.Char(string='Average 401k Contribution Investment ')
	invest_manage_fees = fields.Char(string='Management Fees')
	admin_fees_per_partic = fields.Char(string='Administrative Fees Per Participant')
	redflag_ids = fields.Many2one('strategicchoices.redflag')


class CustomerExtensionTree(models.Model):
	""" MAin FOrm class  """
	_name = 'res.tree'

	full_name = fields.Char(string='Full Name')
	first_name = fields.Char(string='First Name')
	midlle_name = fields.Char(string='Middle Name')
	last_name = fields.Char(string='Last Name')
	suffix = fields.Char(string='Suffix')
	title = fields.Char(string='Title')
	email = fields.Char(string='Email')
	prefix = fields.Selection([('mr','Mr'),('mrs','Mrs')],default='mr',string='Prefix')
	partent_id = fields.Many2one('res.partner')

class BusinessCode(models.Model):
	""" MAin FOrm class  """
	_name = 'business.code'

	name = fields.Char(string='Name')

class PlanName(models.Model):
	""" MAin FOrm class  """
	_name = 'plane.name'

	name = fields.Char(string='Name')

class PensionBenefitCode(models.Model):
	""" MAin FOrm class  """
	_name = 'pension.benefit.code'

	name = fields.Char(string='Name')


