from odoo import models, fields, api
from datetime import datetime, date, timedelta

class PartnerLedgerReport(models.AbstractModel):
	_name = 'report.funds_availability.funds_availability_report'

	@api.model
	def render_html(self,docids, data=None):

		report_obj = self.env['report']
		report = report_obj._get_report_from_name('funds_availability.funds_availability_report')
		active_wizard = self.env['funds.availability'].search([])
		emp_list = []
		for x in active_wizard:
			emp_list.append(x.id)
		emp_list = emp_list
		emp_list_max = max(emp_list) 

		record_wizard = self.env['funds.availability'].search([('id','=',emp_list_max)])
		record_wizard_del = self.env['funds.availability'].search([('id','!=',emp_list_max)])
		record_wizard_del.unlink()

		date = record_wizard.date

		banks = self.env['account.account'].search([('user_type_id.name','=','Bank and Cash')])

		parties = self.env['res.partner'].search([])

		sales = []
		purchases = []

		for x in parties:
			debit = 0
			credit = 0
			party_ledger = self.env['account.move.line'].search([('account_id.name','=','Party Ledger'),('partner_id.id','=',x.id),('move_id.date','<',date),('move_id.state','=', 'posted')])
			
			for y in party_ledger:
				debit = debit + x.debit
				credit = credit + x.credit

			amount = debit - credit

			if amount > 0:
				sale_data = self._prepare_SP_data(x, amount)
				sales.append(sale_data)

			if amount < 0:
				purchase_data = self._prepare_SP_data(x, amount)
				purchases.append(purchase_data)

		def bank_amount(attr):
			debit = 0
			credit = 0
			move_lines = self.env['account.move.line'].search([('account_id.id','=',attr.id),('move_id.date','<',date),('move_id.state','=', 'posted')])
			for x in move_lines:
				debit = debit + x.debit
				credit = credit + x.credit

			return (debit - credit)
			
		docargs = {
			'doc_ids': docids,
			'doc_model': 'res.partner',
			'data': data,
			'banks': banks,
			'bank_amount': bank_amount,
			'sales': sales,
			'purchases': purchases,
			'date': date
		}

		return report_obj.render('funds_availability.funds_availability_report', docargs)



	def _prepare_SP_data(self,data, amount):
		return {
		'name' : data.name,
		'amount' : amount
		}