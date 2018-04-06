from openerp import models, fields, api

class SampleDevelopmentReport(models.AbstractModel):
    _name = 'report.omer_daily_shipment_report.module_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('omer_daily_shipment_report.module_report')
        records = self.env['ufc.auto'].browse(docids)

        def dategetter():
            for x in records:
                dater = x.invoice_date
            return dater

        def namer():
            print "--------------"
            prov = ""
            for x in records:
                if x.customer.name == "ORIENT ELECTRONICS":
                    prov = x.customer.name
                if x.customer.name == "FFC Goth Machi":
                    prov = x.customer.name
                if x.customer.name == "FFC Mir Pur Mathelo":
                    prov = x.customer.name
                if x.customer.name == "Engro Fertilizer Dharki":
                    prov = x.customer.name
                if x.customer.name == "Engro Port Karachi":
                    prov = x.customer.name


            return prov

        docargs = {
            'doc_ids': docids,
            'doc_model': 'ufc.auto',
            'docs': records,
            'data': data,
            'dategetter': dategetter,
            'namer': namer
            }

        return report_obj.render('omer_daily_shipment_report.module_report', docargs)