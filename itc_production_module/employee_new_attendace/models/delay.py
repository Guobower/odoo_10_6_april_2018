from odoo import models, fields, api


class DelayStructure(models.Model):
    _name = 'delay.structure'
    _rec_name = 'name'
    _inherit = 'mail.thread'
    name = fields.Char(string='Name', required=True)
    delay_type = fields.Selection(selection=[('month', 'Monthly Based'), ('hours', 'Hourly Based')],
                                  string='Delay Template',
                                  required=True, default='month')
    min_hours = fields.Float(string='Min hour per schedule')
    penalty_rate = fields.Float(string='Penalty Rate * x delay')
    delay_rules = fields.One2many(comodel_name='delay.rules', inverse_name='structure_id', string='Delay Rules')
    absence_rate = fields.Float(string='Absence Rate')
    no_sign_in_out_rate = fields.Float(string='No Sign In or Sign out Rate')


DelayStructure()


class DelayRules(models.Model):
    _name = 'delay.rules'
    _inherit = 'mail.thread'
    _rec_name = 'name'
    structure_id = fields.Many2one(comodel_name='delay.structure', string='Structure')
    name = fields.Char(string='Name', required=True)
    delay_period_from = fields.Float(string='Delay Period From')
    delay_period_to = fields.Float(string='Delay Period To')
    exempted_minutes = fields.Float(string='Deduction Minutes.')
    action = fields.Selection(selection=[('in', 'Sign In'), ('out', 'Sign Out')], string='For Action')


DelayRules()
