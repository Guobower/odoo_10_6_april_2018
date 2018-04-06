# -*- coding: utf-8 -*- 
from odoo import models, fields, api

class employee_extension(models.Model): 
    _inherit = 'hr.employee'

    ntn = fields.Char(string="NTN Number")
    identification_id = fields.Char(string="CNIC No")

    