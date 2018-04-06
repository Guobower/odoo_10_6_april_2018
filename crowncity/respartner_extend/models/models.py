# -*- coding: utf-8 -*-

from odoo import models, fields, api

class respartner_extend(models.Model):
    _inherit  = 'res.partner'
    plot_property_dealer = fields.Boolean(string="Property Dealer")
    plot_priority_client = fields.Boolean(string="Priority Client")