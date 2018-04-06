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
        mill_loaded = record_wizard.mill_loaded

        sales_opening = self.env['stock.open.line'].search([('date','>=',form),('date','<=',to),('mill.id','=',mill.id),('party.id','=',partner_wiz.id),('types','=','sale')])

        purchase_opening = self.env['stock.open.line'].search([('date','>=',form),('date','<=',to),('mill.id','=',mill.id),('party.id','=',partner_wiz.id),('types','=','purchase')])
        
        sales_open = 0
        for x in sales_opening:
            sales_open = sales_open + x.qty
        
        purch_open = 0
        for x in purchase_opening:
            purch_open = purch_open + x.qty

        purchases = self.env['purchase.sugar'].search([('date','>=',form),('date','<=',to),('supplier.id','=',partner_wiz.id),('mill.id','=',mill.id)])

        sales = self.env['sales.sugar'].search([('date','>=',form),('date','<=',to),('customer.id','=',partner_wiz.id),('mill.id','=',mill.id)])

        transfers = self.env['loading.sugar.tree'].search([('date','>=',form),('date','<=',to),'|',('party.id','=',partner_wiz.id),('to.id','=',partner_wiz.id),('mill.id','=',mill.id)])

        if mill_loaded == False:
            loadings = self.env['loading.adda.tree'].search([('date','>=',form),('date','<=',to),('party.name','=',partner_wiz.name),('mill.id','=',mill.id)])

        if mill_loaded == True:
            loadings = self.env['loading.adda.tree'].search([('date','>=',form),('date','<=',to),('mill_loaded.name','=',partner_wiz.name),('mill.id','=',mill.id)])

        def getopening():

            purchases = self.env['purchase.sugar'].search([('date','<',form),('supplier.id','=',partner_wiz.id),('mill.id','=',mill.id)])

            sales = self.env['sales.sugar'].search([('date','<',form),('customer.id','=',partner_wiz.id),('mill.id','=',mill.id)])

            purchase = 0
            sale = 0

            for x in purchases:
                purchase = purchase + x.qty

            for x in sales:
                sale = sale + x.qty

            opening = (purch_open + purchase) - (sale + sales_open)

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
                if x.transfer_type == "c2c":
                    if x.party.id == partner_wiz.id:
                        transfer = transfer - x.qty

                    if x.to.id == partner_wiz.id:
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

        def load_opens():

            load_purchase = self.env['purchase.sugar'].search([('supplier.id','=',partner_wiz.id),('mill.id','=',mill.id),('date','<',form)])

            load_loadings = self.env['loading.adda.tree'].search([('mill_loaded.name','=',partner_wiz.name),('mill.id','=',mill.id),('date','<',form)])

            purchases = 0
            loadings = 0

            for x in load_purchase:
                purchases = purchases + x.qty

            for x in load_loadings:
                loadings = loadings + x.qty

            return (purchases - loadings)

        def load_current():
            
            current_loadings = self.env['loading.adda.tree'].search([('date','>=',form),('date','<=',to),('mill_loaded.name','=',partner_wiz.name),('mill.id','=',mill.id)])

            loadings = 0
            for x in current_loadings:
                loadings = loadings + x.qty

            return loadings


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
            'loading': loading,
            'mill_loaded': mill_loaded,
            'load_opens': load_opens,
            'load_current': load_current,
        }

        return report_obj.render('stock_movement_report.stock_movement_report', docargs)