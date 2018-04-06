# -*- coding: utf-8 -*- 
from odoo import models, fields, api
from openerp.exceptions import Warning, ValidationError

class invoice_extension(models.Model): 
    _inherit = 'account.invoice'

    invoice_address = fields.Char(string = "Invoice Address")
    port = fields.Char(string = "Discharging Port")
    loading_port = fields.Char(string = "Loading Port")
    bl_no = fields.Char(string = "B/L No.")
    vessel = fields.Char(string = "Vessel")
    container = fields.Char(string = "Coantainer #")
    ship_mark = fields.Char(string = "Ship. Mark")
    performa = fields.Char(string = "Proforma #")
    sro = fields.Char(string = "SRO #")
    s_tax_serial = fields.Char(string = "S Tax Serial")
    cnic = fields.Char(string = "CNIC no")
    ntn = fields.Char(string = "NTN Number")
    style = fields.Char(string = "Style")
    Color = fields.Char(string = "Color")
    qty_ctn = fields.Char(string = "Qty/CTN")
    lot = fields.Char(string = "Lot")
    pin = fields.Char(string = "PIN #")
    partial_shipment = fields.Char(string = "Partial Shipment")
    transhipment = fields.Char(string = "Transhipment")
    e_form_no = fields.Char(string = "E Form No")
    no_of_cartons = fields.Char(string = "Number of Cartons")
    shipment_of = fields.Char(string = "Shipment of")
    airport_departure = fields.Char(string = "Departure Airport")
    airport_designation = fields.Char(string = "Designation Airport")
    origin_goods = fields.Char(string = "Origin of Goods")
    gross_weight = fields.Char(string = "Gross Weight")
    net_weight = fields.Char(string = "Net Weight")
    volume = fields.Char(string = "Volume")
    company = fields.Char("Company")
    remarks = fields.Char("Remarks")
    under_claim = fields.Char("Under Claim For Rebate")
    airline = fields.Char("Airline")
    des = fields.Char("Description")
    carton_size = fields.Char("Carton Size")
    frieght = fields.Char("Frieght")
    hawb_no = fields.Char("H.A.W.B No")
    mawb_no = fields.Char("M.A.W.B No")
    LC_no = fields.Char("LC No")
    HS_code = fields.Char("HS Code")
    manual_serial_no = fields.Char("Manual Serial #")
    awb_no = fields.Char("AWB No.")
    flight_no = fields.Char("Flight No.")
    awb_issued = fields.Char("AWB Issued By")
    customer_order_no = fields.Char("Customer order Number")
    cn = fields.Char("Documentary Credit Number")

    ship_to_address = fields.Text(string = "Ship To Address")
    bill_to_address = fields.Text(string = "Bill To Address")
    notify = fields.Text(string = "Notify")
    other_notify = fields.Text(string = "Other Notify")
    description = fields.Text("Description of Goods or Services Comments")
    narration_1 = fields.Text("Narration for LC (I)")
    narration_2 = fields.Text("Narration for LC (II)")
    through_1 = fields.Text("Through")
    applicant = fields.Text("Applicant")
    rebate_percentage = fields.Text("Rebate Percentage")
    more_info = fields.Text("More Info")

    gross_weight = fields.Float(string = "Gross Weight")
    net_weight = fields.Float(string = "Net Weight")
    Lc_amt = fields.Float("LC Amt")

    etd_khi = fields.Date(string = "ETD KHI")
    eta = fields.Date(string = "ETA")    
    bl_date = fields.Date(string = "B/L Date")
    form_e_date = fields.Date(string = "Form E Date")
    delivery_date = fields.Date(string = "Delivery Date")
    confirmation_date = fields.Datetime(string = "Confirmation Date")
    hawb_date = fields.Date("H.A.W.B Date")
    mawb_date = fields.Date("M.A.W.B Date")
    Lc_date = fields.Date("LC Date")
    manual_date = fields.Date("Manual Date")
    awb_date = fields.Date("AWB Date")
    cn_date = fields.Date("Documentary Credit Number Date")

    invoice_bank = fields.Many2one('res.bank',string = "Bank")
    bank_account = fields.Many2one('res.bank',string = "Bank")
    employee_name = fields.Many2one('hr.employee',string = "Employee Name")
    inco_terms = fields.Many2one('stock.incoterms',string = "Inco Terms")

    data_coming = fields.One2many('other.charges','data_sending')
    data_comes = fields.One2many('third.party','data_sends')
    sale_order_num = fields.Many2one('sale.order',string="Sale Order")

    ma_Bill = fields.Integer("Master Airway Bill #")
    air_freight = fields.Integer("Air Freight")

    ship_via = fields.Selection([
        ('bysea', 'By Sea'),
        ('byair', 'By Air'),
        ('byland', 'By Land'),
        ],default = 'bysea', string = "Ship via")
    ship_mode = fields.Selection([
        ('bysea', 'By Sea'),
        ('byair', 'By Air'),
        ('byland', 'By Land'),
        ],default = 'bysea', string = "Ship Mode")
                
    @api.onchange('employee_name')
    def undertacker(self):
        if self.employee_name:
            self.cnic = self.employee_name.identification_id
            self.ntn = self.employee_name.ntn

    def packing_list(self):

        packing_list = self.env['commercial.packing.list'].search([])

        all_products = []
        for x in self.invoice_line_ids:
            print x.product_id.product_tmpl_id.article_num.id
            print "-----------------------------------------"
            all_products.append((4,x.product_id.product_tmpl_id.article_num.id))

        for x in packing_list:
            if x.invoice_no.id == self.id:
                raise ValidationError("Packing List for this Invoice already created")

        create_packing_list = packing_list.create({
            'invoice_no': self.id,
            'invoice_date': self.date_invoice,
            'e_form': self.e_form_no,
            'e_date': self.form_e_date,
            'notify_to': self.notify,
            'ship_to': self.ship_to_address,
            'awb_no': self.awb_no,
            'awb_date': self.awb_date,
            'lc_no': self.LC_no,
            'lc_date': self.Lc_date,
            'shipment': self.shipment_of,
            'customer_order_no': self.customer_order_no,
            'total_no_carton': self.no_of_cartons,
            'gross_weight': self.gross_weight,
            'grand_total': self.amount_total,
            'carton_size': self.carton_size,
            'delivery_date': self.delivery_date,
            'records': all_products,
            'issue_to': self.partner_id.name,
            })


class other_charges(models.Model): 
    _name = 'other.charges'

    s_no = fields.Char(string = "S/No")
    charges = fields.Char(string = "Charges Description")
    amount = fields.Float(string = "Amount")
    data_sending = fields.Many2one('account.invoice')

class third_party(models.Model): 
    _name = 'third.party'

    s_no = fields.Char(string = "S/No")
    charges = fields.Char(string = "Charges Description")
    amount = fields.Float(string = "Amount")
    data_sends = fields.Many2one('account.invoice')