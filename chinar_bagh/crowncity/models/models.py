# -*- coding: utf-8 -*-

from odoo import models, fields, api

class cust_form_custom(models.Model):
    _inherit = 'res.partner'

    father_name = fields.Char(string="Father/Husband's Name")
    cnic_no = fields.Char(string="CNIC #")
    postal_address = fields.Text(string="Postal Address")
    mobile_no = fields.Char(string="Mobile")
    phone_office = fields.Char(string="Phone Number (Office)")
    phone_res = fields.Char(string="Phone Number (Res)")
    nom_name = fields.Char(string="Name")
    nom_father_name = fields.Char(string="Father / Husband /Guardian")
    nom_cnic = fields.Char(string="CNIC#")
    nom_blood_rel = fields.Char(string="Blood Relation")
    photograph =  fields.Binary(string="2 Passport Size photographs")
    cnic_copy =  fields.Binary(string="CNIC Copy")
    nom_photo_cnic =  fields.Binary(string="Nominated Person's CNIC Copy")




    @api.multi
    def import_photograph(self):
        fileobj = TemporaryFile('w+')
        fileobj.write(base64.decodestring(photograph))
        return

    def import_cnic_copy(self):
        fileobj = TemporaryFile('w+')
        fileobj.write(base64.decodestring(cnic_copy))
        return
    
    def import_nom_photo_cnic(self):
        fileobj = TemporaryFile('w+')
        fileobj.write(base64.decodestring(nom_photo_cnic))
        return



class prod_tmp_custm(models.Model):
    _inherit = 'product.template'

    plot_no = fields.Integer(string="Plot Number")
    street_no = fields.Integer(string="Street Number")
    plot_priority = fields.Char(string="Plot Priority")
    normal = fields.Boolean(string="Normal")
    corner = fields.Boolean(string="Corner (Extra 10 %)")
    boulevard = fields.Boolean(string="Boulevard (10%)")
    park_facing = fields.Boolean(string="Park Facing (Extra 10%)")
    extra_land = fields.Char(string="Extra Land")
    extra_price = fields.Float(string="Extra Price")
    total_price = fields.Float(string="Total Price")


