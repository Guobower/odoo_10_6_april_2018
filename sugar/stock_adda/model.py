from odoo import models, fields, api
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from openerp.exceptions import Warning

class StockMovementAddaWise(models.AbstractModel):
    _name = 'report.stock_adda.stock_adda_report'

    @api.model
    def render_html(self,docids, data=None):

        report_obj = self.env['report']
        report = report_obj._get_report_from_name('stock_adda.stock_adda_report')
        active_wizard = self.env['stock.movement.addas'].search([])
        emp_list = []
        for x in active_wizard:
            emp_list.append(x.id)
        emp_list = emp_list
        emp_list_max = max(emp_list) 

        record_wizard = self.env['stock.movement.addas'].search([('id','=',emp_list_max)])
        record_wizard_del = self.env['stock.movement.addas'].search([('id','!=',emp_list_max)])
        record_wizard_del.unlink()

        to = record_wizard.to
        form = record_wizard.form
        mill = record_wizard.mill
        adda_field = record_wizard.adda_field

        transfers = self.env['loading.sugar.tree'].search([('date','>=',form),('date','<=',to),('adda.id','=',adda_field.id),('mill.id','=',mill.id),('transfer_type','in',["c2g","g2g"])])

        loadings = self.env['loading.adda.tree'].search([('date','>=',form),('date','<=',to),('adda.id','=',adda_field.id),('mill.id','=',mill.id)])

        records = self.env['stock.movement.tree'].search([])

        def bal():
            stockin = 0
            stockout = 0
            openings = 0

            transfers = self.env['loading.sugar.tree'].search([('date','<',form),('adda.id','=',adda_field.id),('mill.id','=',mill.id),('transfer_type','=','g2c')])

            loadings = self.env['loading.adda.tree'].search([('date','<',form),('adda.id','=',adda_field.id),('mill.id','=',mill.id)])

            for x in transfers:
                stockin = stockin + x.qty

            for x in loadings: 
                stockout = stockout + x.qty

            openings = stockin - stockout

            return openings

        docargs = {
            'doc_ids': docids,
            'doc_model': 'res.partner',
            'docs': records,
            'data': data,
            'form': form,
            'to': to,
            'adda_field': adda_field,
            'mill': mill,
            'loadings': loadings,
            'transfers': transfers,
            'bal': bal
        }

        return report_obj.render('stock_adda.stock_adda_report', docargs)