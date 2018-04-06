# -*- coding: utf-8 -*-
# 
#    OpenERP, Open Source Management Solution

#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#

from openerp import models, fields, api, _, SUPERUSER_ID
from datetime import datetime, timedelta


class procurement_order(models.Model):
    _inherit = 'procurement.order'

    production_ids = fields.One2many('mrp.production','procurement_id', 'Manufacturing Orders')

    # def make_mo(self, cr, uid, ids, context=None):
    #     """ Make Manufacturing(production) order from procurement
    #     @return: New created Production Orders procurement wise
    #     """
    #     res = {}
    #     production_obj = self.pool.get('mrp.production')
    #     procurement_obj = self.pool.get('procurement.order')
    #     for procurement in procurement_obj.browse(cr, uid, ids, context=context):
    #         if self.check_bom_exists(cr, uid, [procurement.id], context=context):
    #             # create the MO as SUPERUSER because the current user may not have the rights to do it (mto product launched by a sale for example)
    #             vals = self._prepare_mo_vals(cr, uid, procurement, context=context)
    #             product_qty = int(procurement.product_qty)
    #             for qty in range(product_qty):
    #                 vals['product_qty'] = 1
    #                 vals['procurement_id'] = procurement.id
    #                 produce_id = production_obj.create(cr, SUPERUSER_ID, vals,
    #                                                context=dict(context, force_company=procurement.company_id.id))
    #                 res[procurement.id] = True
    #                 production_obj.action_compute(cr, uid, [produce_id], properties=[x.id for x in procurement.property_ids])
    #                 production_obj.signal_workflow(cr, uid, [produce_id], 'button_confirm')
    #             self.production_order_create_note(cr, uid, procurement, context=context)
    #         else:
    #             res[procurement.id] = False
    #             self.message_post(cr, uid, [procurement.id], body=_("No BoM exists for this product!"), context=context)
    #     return res


    # def production_order_create_note(self, cr, uid, procurement, context=None):
    #     name = ''
    #     for production in procurement.production_ids:
    #         name += production.name
    #         name += ','

    #     body = _("Manufacturing Order <em>%s</em> created.") % (name,)
    #     self.message_post(cr, uid, [procurement.id], body=body, context=context)

    # def _check(self, cr, uid, procurement, context=None):
    #     Flag = False
    #     if procurement.production_ids:
    #         for production_id in procurement.production_ids:
    #             if production_id and procurement.production_id.state != 'done':  # TOCHECK: no better method?
    #                 Flag = True
    #         if not Flag:
    #             return True
    #     return super(procurement_order, self)._check(cr, uid, procurement, context=context)

