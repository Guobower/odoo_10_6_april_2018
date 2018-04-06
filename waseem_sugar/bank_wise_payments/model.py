from odoo import models, fields, api
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from openerp.exceptions import Warning

class PartnerLedgerReport(models.AbstractModel):
    _name = 'report.bank_wise_payments.bank_wise_report'

    @api.model
    def render_html(self,docids, data=None):

        report_obj = self.env['report']
        report = report_obj._get_report_from_name('bank_wise_payments.bank_wise_report')
        active_wizard = self.env['bank.wise.payments'].search([])
        records = self.env['res.partner'].browse(docids)
        emp_list = []
        for x in active_wizard:
            emp_list.append(x.id)
        emp_list = emp_list
        emp_list_max = max(emp_list) 

        record_wizard = self.env['bank.wise.payments'].search([('id','=',emp_list_max)])
        record_wizard_del = self.env['bank.wise.payments'].search([('id','!=',emp_list_max)])
        record_wizard_del.unlink()

        to = record_wizard.to
        form = record_wizard.form
        typed = record_wizard.entry_type
        partner_wiz = record_wizard.partner

        if typed == "posted":
            funds = self.env['funds.flow.tree'].search([('date_confirmation','>=',form),('date_confirmation','<=',to),'|',('party.id','=',partner_wiz.id),('supplier.id','=',partner_wiz.id),('type_transaction','in',["bp","jv"]),('stages','=','confirmation')])

        if typed == "all":
            funds = self.env['funds.flow.tree'].search([('date','>=',form),('date','<=',to),'|',('party.id','=',partner_wiz.id),('supplier.id','=',partner_wiz.id),('type_transaction','in',["bp","jv"])])


        banks = []
        climb = []
        for x in funds:
            if x.type_transaction == "jv":
                bank = x.supplier_bank.name
                if bank not in banks:
                    banks.append(bank)

            if x.type_transaction == "bp":
                bank = x.banks_pakistan.name
                if bank not in banks:
                    banks.append(bank)

        def getbank(record):
            if record.type_transaction == "jv":
                banks = record.supplier_bank.name

            if record.type_transaction == "bp":
                banks = record.banks_pakistan.name

            print banks
            print record.amount
            print "------------------------"
            return banks
            
        docargs = {
            'doc_ids': docids,
            'doc_model': 'res.partner',
            'docs': records,
            'data': data,
            'form': form,
            'to': to,
            'partner_wiz': partner_wiz,
            'banks': banks,
            'funds': funds,
            'getbank': getbank,
            'typed': typed
        }

        return report_obj.render('bank_wise_payments.bank_wise_report', docargs)