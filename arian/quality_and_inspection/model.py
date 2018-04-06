# -*- coding: utf-8 -*- 
from odoo import models, fields, api
from openerp.exceptions import Warning, ValidationError

class quality_inspection(models.Model):
    _name = 'quality.inspection'
    _rec_name = 'q_po_no'

    q_to=fields.Char("To :")
    q_to_faxmail=fields.Char("Fax/ E-mail To:")
    q_cc_faxmail=fields.Char("Fax/ E-mail Cc:")
    q_from_faxmail=fields.Char("Fax/ E-mail From:")
    q_attn=fields.Char("Attn :")
    q_cc=fields.Char("Cc :")
    q_from=fields.Char("From :")
    q_file_no=fields.Char("File No. :")
    q_date=fields.Date("Date :")
    q_registration_no=fields.Char("Registration No. :")
    q_buyer=fields.Char("Buyer :")
    q_po_no=fields.Char("P.O. no. :") 
    q_agent=fields.Char("Agent :")
    q_lc_no=fields.Char("L/C no. :")
    q_supplier=fields.Char("Supplier")
    q_total_pages=fields.Char("Total pages:")
    q_manufacturer=fields.Char("Manufacturer :")
    q_product_des=fields.Char("Product Description :")
    q_inspection_type_performed=fields.Char("Inspection type performed :")
    q_inspection_date=fields.Date("Inspection date :")
    q_inspection_location=fields.Char("Inspection location :")
    quality_inspection_tree_link=fields.One2many('quality.inspection.tree','quality_inspections_tree')
    inspection_conclusion_tree_link=fields.One2many('inspection.conclusion.tree','inspection_conclusion_tree')
    wokrmanship_appearance_tree_link=fields.One2many('wokrmanship.appearance.tree','wokrmanship_appearance_tree')
    packing_tree_link=fields.One2many('packing.tree','packing_tree')
    q_aql_critical=fields.Integer("Critical: ")
    q_aql_major=fields.Integer("Major: ")
    q_aql_minor=fields.Integer("Minor: ")
    q_ssf=fields.Char("Sample Selection formula: ")
    q_carton=fields.Integer("No. of Cartons:")
    q_ssi=fields.Integer("Sample size inspected:")
    q_selected_samples=fields.Char("Samples selected from carton numbers:")
    q_data_samples=fields.Char("Data measurement / field test on sub-samples:")
    q_repack_close=fields.Char("Re packed cartons identified by stamps / closing tape:")
    q_critical_defective=fields.Integer("Critical defective maximum allowed")
    q_major_defective=fields.Integer("Major defective maximum allowed")
    q_minor_defective=fields.Integer("Minor defective maximum allowed")
    q_critical_defective_allow=fields.Integer("Actual")
    q_major_defective_allow=fields.Integer("Actual")
    q_minor_defective_allow=fields.Integer("Actual")
    q_packing_detalis=fields.Text("Packing Detials")
    q_carton_size=fields.Char("Carton Size")
    q_packing_assortment=fields.Char("Packing assortment Checked on")

    q_overall=fields.Selection([
        ('notconform','Not Conform'),
        ('actual','Actual')
        ],string="OVERALL INSPECTION CONCLUSION :")
    q_style_conformity=fields.Selection([
        ('not_conform','Not Conform'),
        ('actual','Actual')
        ],string="1.1 Style Conformity:")
    q_material_conformity=fields.Selection([
        ('not_conform','Not Conform'),
        ('actual','Actual')
        ],string="1.2 Material Conformity:")
    q_colour_conformity=fields.Selection([
        ('not_conform','Not Conform'),
        ('actual','Actual')
        ],string="1.3 Colour Conformity:")
    q_reference_sample=fields.Selection([
        ('vailable','Available'),
        ('not_available',' Not Available')
        ],string="Reference sample provided")
    q_individual_packing=fields.Selection([
        ('yes','Yes'),
        ('no',' No')
        ],string="Individual packing conformity")
    q_inner_packing=fields.Selection([
        ('yes','Yes'),
        ('no',' No')
        ],string="Inner packing conformity")
    q_export_packing=fields.Selection([
        ('yes','Yes'),
        ('no',' No')
        ],string="Export packing conformity")

class inspection_conclusion_tree(models.Model):

    _name = 'inspection.conclusion.tree'
    q_des=fields.Char("Description")
    q_status=fields.Char("Status")
    q_remaks=fields.Char("Remakrs")
    inspection_conclusion_tree=fields.Many2one('quality.inspection')

class wokrmanship_appearance_tree(models.Model):

    _name = 'wokrmanship.appearance.tree'
    wa_defective_samples=fields.Integer("Defective samples")
    wa_aql_critical=fields.Integer("Critical: ")
    wa_aql_major=fields.Integer("Major: ")
    wa_aql_minor=fields.Integer("Minor: ")
    wokrmanship_appearance_tree=fields.Many2one('quality.inspection')

class packing_tree(models.Model):

    _name = 'packing.tree'
    pt_carton_no=fields.Integer("Carton No")
    pt_size_style=fields.Char("Size / Style")
    pt_colour=fields.Char("Colour")
    pt_deviation=fields.Char("Deviation (+ / - samples)")
    packing_tree=fields.Many2one('quality.inspection')

class quality_inspection_tree(models.Model):

    _name = 'quality.inspection.tree'
    qt_style_item_article=fields.Char("Style/Item/Article")
    qt_ordered=fields.Integer("Ordered")
    qt_declared=fields.Integer("Declared")
    qt_cartons=fields.Integer("No. of Cartons")
    qt_colour=fields.Char("Colour")
    qt_status=fields.Char("Status")
    quality_inspections_tree=fields.Many2one('quality.inspection')

class product_quality_note(models.Model): 
    _name = 'quality.note'
    _rec_name= 'prod_customer'

    prod_customer = fields.Many2one('res.partner',string="Customer", domain=[('customer','=',True)] )

    style = fields.Char(string="Style")
    m_order = fields.Char(string="MO #")
    date = fields.Date(string="Date")
    quality_note_tree_link=fields.One2many('quality.note.tree','quality_note_tree')

    @api.onchange('prod_customer')
    def onchange_prod_customer(self):
        if self.prod_customer:
            delete = []
            delete = delete.append(2)
            self.quality_note_tree_link = delete

class product_quality_note_tree(models.Model):
    _name = 'quality.note.tree'

    product = fields.Many2one('product.template',string="Products" )
    material_des=fields.Char(string="Material Description")
    workmanship_des=fields.Char(string="Workmanship Description")
    decor_des=fields.Char(string="Decor Description")
    packing_des=fields.Char(string="Packing Description")
    comments=fields.Text(string="Comments")

    quality_note_tree=fields.Many2one('quality.note')

    @api.onchange('product')
    def onchange_product(self):
        if self.product:

            name_prod=self.product.name
            customer_products = self.env['product.template'].search([('name','=',name_prod)])

            self.material_des= customer_products.material_descrip
            self.workmanship_des=customer_products.workmanship_descrip
            self.decor_des=customer_products.decor_descrip
            self.packing_des=customer_products.packing_descrip

class commercial_packing_list(models.Model):
    _name = 'commercial.packing.list'
    _rec_name = 'invoice_no'

    issue_to=fields.Char("Issed To")
    invoice_no=fields.Many2one("account.invoice", string="Invoice No")
    invoice_date=fields.Date("Invoice Dated")
    e_form=fields.Char("E-Form No")
    e_date=fields.Date("E-Form Date")
    notify_to=fields.Text("Notify To")
    ship_to=fields.Text("Ship To")
    awb_no=fields.Char("A.W.B No")
    awb_date=fields.Date("A.W.B Date")
    lc_no=fields.Char("L/C No")
    lc_date=fields.Date("L/C Date")
    shipment=fields.Char("Shipment of")
    customer_order_no=fields.Char("Customer Order No")
    total_no_carton=fields.Integer("Total No of Carton")
    grand_total=fields.Integer("Grand Total")
    gross_weight=fields.Float("Gross Weight")
    carton_size=fields.Char("Carton Size")
    net_weight=fields.Float("Net Weight")
    volume=fields.Float("Volume")
    commercial_packing_list_tree_link=fields.One2many('commercial.packing.list.tree','commercial_packing_list_tree')
    records = fields.Many2many('product.artical',string="records")

    cn=fields.Char("Documentary Credit Number#")
    cn_date=fields.Date("Documentary Credit Date")
    delivery_date = fields.Date("Shipment Date")

    ship_mark=fields.Char("Shipping Mark")
    supplier_code=fields.Char("Supplier Code")

    @api.onchange('invoice_no')
    def onchange_product(self):
        if self.invoice_no:

            name_invoice = self.invoice_no.number
            
            invoices = self.env['account.invoice'].search([('number','=',name_invoice)])

            self.invoice_date = invoices.date_invoice
            self.e_form = invoices.e_form_no
            self.e_date = invoices.form_e_date
            self.notify_to = invoices.notify
            self.ship_to = invoices.ship_to_address
            self.awb_no = invoices.awb_no
            self.awb_date = invoices.awb_date
            self.lc_no = invoices.LC_no
            self.lc_date = invoices.Lc_date
            self.shipment = invoices.shipment_of
            self.customer_order_no = invoices.customer_order_no
            self.notify_to = invoices.notify
            self.awb_no = invoices.awb_no
            self.awb_date = invoices.awb_date
            self.lc_no = invoices.LC_no
            self.lc_date = invoices.Lc_date
            self.cn = invoices.cn
            self.shipment_of = invoices.shipment_of
            self.cn_date = invoices.cn_date
            self.ship_mark = invoices.ship_mark

    @api.onchange('commercial_packing_list_tree_link')
    def onchange_weight(self):
        self.gross_weight = 0.0
        self.net_weight = 0.0
        self.volume = 0.0
        self.grand_total =0.0
        c_list=[]
        for x in self.commercial_packing_list_tree_link:
            self.net_weight = x.net_weight + self.net_weight
            self.gross_weight = x.gross_weight + self.gross_weight
            self.volume = x.volume + self.volume
            self.grand_total = x.qty + self.grand_total
            if x.carton not in c_list:
                c_list.append(x.carton)

        self.total_no_carton=len(c_list)

    @api.multi
    def write(self, vals):
        res = super(commercial_packing_list,self).write(vals)
        self.invoice_no.no_of_cartons = self.total_no_carton

        if self.commercial_packing_list_tree_link:

            def packing_qty(prod):
                pack_qty = 0
                for x in self.commercial_packing_list_tree_link:
                    if x.prod_name.id == prod:
                        pack_qty = pack_qty + x.qty

                return pack_qty

            def invoice_qty(prod):
                inv_qty = 0
                for x in self.invoice_no.invoice_line_ids:
                    if x.product_id.product_tmpl_id.id == prod:
                        inv_qty = inv_qty + x.quantity

                return inv_qty

            all_product_ids = []
            for x in self.commercial_packing_list_tree_link:
                if x.prod_name.id not in all_product_ids:
                    all_product_ids.append(x.prod_name.id)

            for x in all_product_ids:

                active_prod = x

                if packing_qty(active_prod) > invoice_qty(active_prod):
                    active_prod_name = ' '
                    for y in self.commercial_packing_list_tree_link:
                        if y.prod_name.id == active_prod:
                            active_prod_name = y.prod_name.name
                    raise ValidationError("Quantity of '%s' exceeds its quantity of Invoice" %active_prod_name)
    

        return res

class commercial_packing_list_tree(models.Model): 

    _name = 'commercial.packing.list.tree'

    carton=fields.Integer("No of Carton")
    carton_qty=fields.Integer("Qty/Carton")
    colour=fields.Many2one("product.attribute.value","Color")
    artical_no=fields.Many2one('product.artical',"Artical #")
    prod_name=fields.Many2one("product.template",string= "Product")
    des=fields.Char("Description")
    size=fields.Many2one("product.attribute.value","Size")
    qty=fields.Integer("Qty")
    net_weight=fields.Float("Net Weight")
    gross_weight=fields.Float("Gross Weight")
    volume=fields.Float("Volume")

    commercial_packing_list_tree = fields.Many2one('commercial.packing.list')
    
    
    @api.onchange('artical_no')
    def onchange_artical_no(self):
        if self.artical_no:
            a_d = self.artical_no.id
            artical_desc = self.env['product.template'].search([('article_num.id','=',a_d)])
            self.des = artical_desc.description_sale
            self.prod_name =artical_desc.id

            self.net_weight = artical_desc.net_weight
            self.gross_weight = artical_desc.grossed_weight
            self.volume = artical_desc.counted_volume