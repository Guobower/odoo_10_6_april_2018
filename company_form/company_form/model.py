# -*- coding: utf-8 -*- 
from odoo import models, fields, api

class Companies(models.Model):
	_name = 'contact.companies'
	_inherit = 'res.partner'

	plan_score = fields.Char(string="Plan Score")
	no_of_red_flags = fields.Char(string="# Of Red Flags")
	partic_totals = fields.Char(string="Participants: Total")
	tot_pal_ass = fields.Char(string="Total Plan Assets")
	plan_number = fields.Char(string="Plan Number")
	total_plan_for_ein = fields.Char(string="Total Plan for EIN")

	job_position = fields.Char(string="Job Position")
	phone = fields.Char(string="Phone")
	mobile = fields.Char(string="Mobile")
	website = fields.Char(string="Website")
	naics_code = fields.Many2one('naics.code',string="Business (NAICS) Code")

	name = fields.Char(string="Customer Name")

	sponsor_ein = fields.Char(string="Sponsor EIN")
	plan_number2 = fields.Char(string="Plan Number")
	plan_name = fields.Many2one('plan.name',string="Plan Name")
	splan_renewal = fields.Selection([
		('january', 'January'),
		('february', 'February'),
		('march', 'March'),
		('april', 'April'),
		('may', 'May'),
		('june', 'June'),
		('july', 'July'),
		('august', 'August'),
		('september', 'September'),
		('october', 'October'),
		('november', 'November'),
		('december', 'December'),
		],default='january',string="Plan Renewal Month (1-12)")

	pen_ben_code = fields.Many2one('pension.benefit.code',string="  Pension Benefit Code(s)")
	acc_firm_name = fields.Char(string="Accountant Firm Name")
	annuity_gic_carr_name = fields.Char(string="Annuity/GIC 01: Carrier Name")
	provider_name_01 = fields.Char(string="Provider 01: Provider Name")
	provider_name_02 = fields.Char(string="Provider 02: Provider Name")

	plan_score2 = fields.Char(string="Plan Score")
	partic_total = fields.Char(string="Participants: Total")
	active_total = fields.Char(string="Participants: Active Total")
	partic_rate = fields.Char(string="Participation Rate")
	tot_pal_ass = fields.Char(string="Total Plan Assets")
	rat_of_retu = fields.Char(string="Rate of Return (1 year)")
	rat_of_retu_3 = fields.Char(string="  Rate of Return Over 3 Years")
	rat_of_retu_5 = fields.Char(string="Rate of Return Over 5 Years")
	ave_par_bal = fields.Char(string="Average Participant Balance")
	ave_accou_bal = fields.Char(string="Average Account Balance 1 Year Growth")
	total_contri = fields.Char(string="Total Contributions")
	ave_401_contri = fields.Char(string="Average 401k Contribution")
	invest_manage_fees = fields.Char(string="Investment Management Fees")
	admin_fees_per_partic = fields.Char(string="Administrative Fees Per Participan")
	schedule_meeting = fields.Char(string="meeting")

	redflag_ids = fields.Many2many('strategicchoices.redflag',string="Red Flags")

	contact_address = fields.One2many('address.contacts','address_contact_id')
	annunity_gic_tree = fields.One2many('annuity.gic','annunity_gic_id')
	provider_gic_tree = fields.One2many('provider.info','provider_info_id')

class addrerss_contacts(models.Model): 
	_name = 'address.contacts'

	full_name = fields.Char(string="Full Name", required= True)
	prefix = fields.Selection([
		('mr', 'Mr'),
		('mrs', 'Mrs'),
		],default='mr',string="Prefix")
	first_name = fields.Char(string="First Name")
	middle_name = fields.Char(string="Middle Name")
	last_name = fields.Char(string="Last Name")
	suffix = fields.Char(string="Suffix")
	email = fields.Char(string="Email")
	
	title = fields.Many2one('res.partner.title', string="Title")

	address_contact_id = fields.Many2one('res.partner')

class AnnuityGic(models.Model): 
	_name = 'annuity.gic'

	carrier_name = fields.Char(string="Carrier Name")
	name = fields.Char(string="Participants")
	general_accounts = fields.Char(string="Value of General Accounts")
	separate_accounts = fields.Char(string="Value of Separate Accounts")

	annunity_gic_id = fields.Many2one('res.partner')
	brocker_info_tree = fields.One2many('brocker.info','brocker_info_id')

class BrokerInfo(models.Model): 
	_name = 'brocker.info'

	commissions = fields.Char(string="Broker Commissions")
	name = fields.Char(string="Broker Name")

	brocker_info_id = fields.Many2one('res.partner')

class ProviderInfo(models.Model): 
	_name = 'provider.info'

	name = fields.Char(string="Provider Name")
	dir_com_amount = fields.Char(string="Direct Compensation Amount")
	indir_com_amount = fields.Char(string="Indirect Compensation Amount")
	service_code = fields.Many2one('service.code',string="Service Codes")

	provider_info_id = fields.Many2one('res.partner')

class NAICS(models.Model): 
	_name = 'naics.code'

	name = fields.Char(String="Name")

class PlanName(models.Model): 
	_name = 'plan.name'

	name = fields.Char(String="Name")

class PensionBenefitCode(models.Model): 
	_name = 'pension.benefit.code'

	name = fields.Char(String="Name")

class ServiceCode(models.Model): 
	_name = 'service.code'

	name = fields.Char(String="Name")

class RedFlags(models.Model): 
	_name = 'strategicchoices.redflag'

	name = fields.Char(String="Red Flags")