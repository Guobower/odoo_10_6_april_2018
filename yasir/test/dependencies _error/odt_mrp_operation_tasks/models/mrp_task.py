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

from openerp import models, fields, api, _
from datetime import datetime, timedelta


class ProjectTask(models.Model):
    _inherit= 'project.task'

    # @api.multi
    # def finish_task(self):
    #     flag = True
    #     done_stage = self.env['project.task.type'].search([('name', '=', 'Done')])[0]
    #     self.stage_id = done_stage.id
    #     if self.workorder.work_ids:
    #         for work in self.workorder.work_ids:
    #             if work.task_id.stage_id.name == 'Done' and flag:
    #                 continue
    #             else:
    #                 flag = False
    #         if flag:
    #             return self.workorder.signal_workflow('button_done')

    # @api.onchange('stage_id')
    # def _onchange_stage_id(self):
    #     flag = True
    #     print 'test'
    #     if self.stage_id:
    #         if self.stage_id.name=='Done':
    #             for work in self.workorder.work_ids:
    #                 if work.task_id.stage_id.name =='Done' and flag:
    #                     continue
    #                 else:
    #                     flag = False
    #         if flag:
    #             self.workorder.button_done()
