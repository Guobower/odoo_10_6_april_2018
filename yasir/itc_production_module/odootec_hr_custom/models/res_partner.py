from odoo import models, fields, api
from datetime import datetime, date


class res_partner(models.Model):
    _inherit = 'res.partner'

    @api.one
    @api.depends('birthday')
    def compute_age(self):
        for partner in self:
            if partner.birthday:
                today = fields.date.today()
                born = datetime.strptime(partner.birthday, '%Y-%m-%d')
                self.age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
            else:
                self.age = 0

    name = fields.Char('Name', translate=True, required=True)
    identification_no = fields.Char('National ID/Iqama')
    age = fields.Integer('Age', compute='compute_age')
    birthday = fields.Date('Birth Day')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], 'Gender')
