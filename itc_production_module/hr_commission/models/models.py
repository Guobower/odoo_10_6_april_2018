# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartner(models.Model):
    """Add some fields related to commissions"""
    _inherit = "res.partner"

    agent_type = fields.Selection(
        selection_add=[("salesman", "Salesman (employee)")])
    employee = fields.Many2one(
        comodel_name="hr.employee", compute="_get_employee")
    users = fields.One2many(comodel_name="res.users",
                            inverse_name="partner_id")