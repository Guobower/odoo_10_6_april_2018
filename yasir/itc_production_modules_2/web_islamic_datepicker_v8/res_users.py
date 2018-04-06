from odoo import models, fields, api
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF

class res_users(models.Model):
    
    _inherit = 'res.users'


    calendear_localisation= fields.Selection([('ar','Arabic'),('fa','Farsi')],'Localisation')
    
    

    # def get_calendear_localisation(self, cr, uid, fields=False, context=None):        
    #     user_brow_obj = self.pool.get('res.users').browse(cr,uid,uid,context=context)
    #     res_lang_obj = self.pool.get('res.lang')
    #     lang_ids = res_lang_obj.search(cr,uid,[('code','=',user_brow_obj.lang)])
    #     date_format = '%m/%d/%Y'
    #     if lang_ids:
    #          date_format = res_lang_obj.browse(cr,uid,lang_ids[0],context).date_format        
    #     return {
    #         'lang':self.browse(cr,uid,uid,context).calendear_localisation or '',
    #         'date_format': date_format
    #     }
    
    
        