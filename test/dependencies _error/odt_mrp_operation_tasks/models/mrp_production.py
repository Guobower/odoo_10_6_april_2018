# -*- coding: utf-8 -*-
# 
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 OdooTec (<http://odootec.com>).
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

from openerp import models, fields, api, _
from datetime import datetime, timedelta


class MrpProductionWorkcenterLine(models.Model):
    _inherit = 'mrp.production.workcenter.line'
    @api.model
    def _prepare_tasks_vals(self, workorder, task_vals):
        task_list = []
        if workorder.routing_wc_line.task_ids:
            for task in workorder.routing_wc_line.task_ids:
                vals = task_vals.copy()
                vals['name'] = (
                    _("%s") %
                    task.name)
                task_list.append(vals)
            return task_list
        return []


