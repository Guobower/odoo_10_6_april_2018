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

from openerp import models, api


class ProcurementOrder(models.Model):
    _inherit = 'procurement.order'

    # @api.model
    # def _prepare_mo_vals(self, procurement):
    #     res = super(ProcurementOrder, self)._prepare_mo_vals(procurement)
    #     mrp_route_obj = self.env['mrp.routing']
    #     if res.get('routing_id'):
    #         routing_id = mrp_route_obj.browse(res.get('routing_id'))
    #         if routing_id.supervisor_id:
    #             res['user_id'] = routing_id.supervisor_id.id
    #     return res
