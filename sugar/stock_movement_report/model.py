from odoo import models, fields, api
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from openerp.exceptions import Warning

class PartnerLedgerReport(models.AbstractModel):
    _name = 'report.stock_movement_report.stock_movement_report'

    @api.model
    def render_html(self,docids, data=None):

        report_obj = self.env['report']
        report = report_obj._get_report_from_name('stock_movement_report.stock_movement_report')
        active_wizard = self.env['stock.movement'].search([])
        records = self.env['res.partner'].browse(docids)
        emp_list = []
        for x in active_wizard:
            emp_list.append(x.id)
        emp_list = emp_list
        emp_list_max = max(emp_list) 

        record_wizard = self.env['stock.movement'].search([('id','=',emp_list_max)])
        record_wizard_del = self.env['stock.movement'].search([('id','!=',emp_list_max)])
        record_wizard_del.unlink()

        to = record_wizard.to
        form = record_wizard.form
        mill = record_wizard.mill
        partner_wiz = record_wizard.partner

        purchases = self.env['purchase.sugar'].search([('date','>=',form),('date','<=',to),('supplier.id','=',partner_wiz.id),('mill.id','=',mill.id)])

        sales = self.env['sales.sugar'].search([('date','>=',form),('date','<=',to),('customer.id','=',partner_wiz.id),('mill.id','=',mill.id)])

        transfers = self.env['loading.sugar.tree'].search([('date','>=',form),('date','<=',to),'|',('party.id','=',partner_wiz.id),('to.id','=',partner_wiz.id),('mill.id','=',mill.id)])

        loadings = self.env['loading.adda.tree'].search([('date','>=',form),('date','<=',to),('party.name','=',partner_wiz.name),('mill.id','=',mill.id)])

        def getopening():

            purchases = self.env['purchase.sugar'].search([('date','<',form),('supplier.id','=',partner_wiz.id),('mill.id','=',mill.id)])

            sales = self.env['sales.sugar'].search([('date','<',form),('customer.id','=',partner_wiz.id),('mill.id','=',mill.id)])

            purchase = 0
            sale = 0

            for x in purchases:
                purchase = purchase + x.qty

            for x in sales:
                sale = sale + x.qty

            opening = purchase - sale 

            return opening

        def netpurchase():

            purchase = 0
            sale = 0

            for x in purchases:
                purchase = purchase + x.qty

            for x in sales:
                sale = sale + x.qty

            netpurchase = purchase - sale 

            return netpurchase

        def TranfersIn():
            transfer = 0
            for x in transfers:
                if x.transfer_type == "c2g":
                    transfer = transfer + x.qty

            return transfer

        def TranfersOut():
            transfer = 0
            for x in transfers:
                if x.transfer_type == "c2g":
                    transfer = transfer + x.qty

            return transfer

        def loading():
            loads = 0
            for x in loadings:
                loads = loads + x.qty

            return loads


        def get_transfer_type(typed):
            if typed == "c2g":
                return "Client to Goods"

            if typed == "g2c":
                return "Goods to Client"

            if typed == "c2c":
                return "Client to Client"

            if typed == "g2g":
                return "Goods to Goods"

        docargs = {
            'doc_ids': docids,
            'doc_model': 'res.partner',
            'docs': records,
            'data': data,
            'form': form,
            'to': to,
            'partner_wiz': partner_wiz,
            'mill': mill,
            'purchases': purchases,
            'sales': sales,
            'transfers': transfers,
            'get_transfer_type': get_transfer_type,
            'loadings': loadings,
            'getopening': getopening,
            'netpurchase': netpurchase,
            'TranfersIn': TranfersIn,
            'loading': loading
        }

        return report_obj.render('stock_movement_report.stock_movement_report', docargs)