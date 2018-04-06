from openerp import models, fields, api


class WorkOrder(models.Model):
    _inherit = 'mrp.production.workcenter.line'

    user_id = fields.Many2one(comodel_name='res.users', string='Team Leader')

    # @api.onchange('workcenter_id')
    # def _onchange_workcenter(self):
    #     if self.workcenter_id:
    #         self.user_id = self.workcenter_id.teamleader_id.id


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

#     @api.multi
#     def _prepare_wc_line(self, wc_use, level=0, factor=1):
#         res = super(MrpBom, self)._prepare_wc_line(wc_use, level, factor)
#         user = False
#         if wc_use.workcenter_id:
#             user = wc_use.workcenter_id.teamleader_id.id
#         res['user_id'] = user
#         return res


# WorkOrder()


class Hranalytic(models.Model):
    _inherit = "account.analytic.line"

#     @api.model
#     def create(self, vals):
#         res = super(Hranalytic, self.sudo()).create(vals).with_env(self.env)
#         return res

#     @api.multi
#     def write(self, vals):
#         res = super(Hranalytic, self.sudo()).write(vals)
#         return res

# Hranalytic()


class HrTimesheet(models.Model):
    _inherit = "hr.analytic.timesheet"

#     @api.model
#     def create(self, vals):
#         res = super(HrTimesheet, self.sudo()).create(vals).with_env(self.env)
#         return res

#     @api.multi
#     def write(self, vals):
#         res = super(HrTimesheet, self.sudo()).write(vals)
#         return res


# HrTimesheet()


class ProjectTask(models.Model):
    _inherit = 'project.task'

#     @api.model
#     def create(self, vals):
#         res = super(ProjectTask, self.sudo()).create(vals).with_env(self.env)
#         return res

#     @api.multi
#     def write(self, vals):
#         res = super(ProjectTask, self.sudo()).write(vals)
#         return res


# ProjectTask()
