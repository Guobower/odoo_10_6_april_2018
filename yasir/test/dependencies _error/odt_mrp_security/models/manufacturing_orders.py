from openerp import models, api, SUPERUSER_ID


class ManufacturingOrders(models.Model):
    _inherit = 'mrp.production'

#     @api.multi
#     @api.onchange('user_id')
#     def onchange_user_id(self):
#         line_ids = self.env['mrp.production.workcenter.line'].search([('production_id', '=', self.id)])
#         for record in line_ids:
#             record.write({'user_id': self.user_id.id})

#     @api.onchange('routing_id')
#     def _onchange_routing(self):
#         if self.routing_id:
#             self.user_id = self.routing_id.supervisor_id.id


# ManufacturingOrders()


class MrpProductionWorkcenterLine(models.Model):
    _inherit = 'mrp.production.workcenter.line'

#     def action_start_working(self, cr, uid, ids, context=None):
#         return super(MrpProductionWorkcenterLine, self).action_start_working(cr, SUPERUSER_ID, ids, context=context)


# MrpProductionWorkcenterLine()
