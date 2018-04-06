# -*- coding: utf-8 -*- 
from odoo import models, fields, api

class struct_user_extend(models.Model):
	_inherit  = 'res.users'
	branch = fields.Many2one ('branch',string="Branch")


class branchAAA(models.Model):
	_name = 'branch'

	address = fields.Char(string="Address")
	name = fields.Char(string="Name")
	phone = fields.Char(string="Phone")
	mobile = fields.Char(string="Mobile")