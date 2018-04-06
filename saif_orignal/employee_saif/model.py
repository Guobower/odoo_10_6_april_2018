# -*- coding: utf-8 -*- 
import psycopg2


from odoo import models, fields, api

class MB_Project_Extension(models.Model):
	_inherit = 'hr.employee'

	f_name = fields.Char("Father Name")
	cnic = fields.Char("CNIC")
	city_id = fields.Char("City")
	country = fields.Char("Country")
	religion = fields.Char("Religion")
	doj = fields.Date("D.O.J",required=True)
	e_contact = fields.Char("Contact")
	per_address = fields.Text("Permanent Address")
	tem_address = fields.Text("Temporary Address")
	emp_link = fields.One2many('ext.employee','emp_filed')
	seq_id = fields.Char(string="Employee Sequence",readonly=True)
	gender = fields.Selection(
		[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], string="Gender")
	marital = fields.Selection(
		[('Single', 'Single'), ('Married', 'Married'), ('Widower', 'Widower'),('Divorced', 'Divorced')], string="Marital Status")


	@api.model
	def create(self, vals):
		vals['seq_id'] = self.env['ir.sequence'].next_by_code('mem.seq')
		new_record = super(MB_Project_Extension, self).create(vals)

		return new_record


	@api.multi
	def data_base(self):
		try:
			conn = psycopg2.connect("dbname='logistic_vision' user='postgres' host='localhost' password='postgres'")
		except:
			print "I am unable to connect to the database"
		cur = conn.cursor()
		cur.execute(""" SELECT * FROM account_invoice""")
		result1 = cur.fetchall()
		for x in result1:
			print type(x)
			print x[0]
			print "kkkkkkkkkkkkkkkkkkkkkkk"
			cr = self.env.cr
			cr.execute(" INSERT INTO account_invoice (id,create_date,journal_id,partner_id,company_id,account_id,reference_type,currency_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(x[0],x[3],5,7,x[16],1,x[26],x[37]))
		# cr.execute(""" select * from nayyab_Inspiron_N4050.logistic_vision.dbo.account_invoice""")
		# result = cr.fetchall()
		# print result
		print "kkkkkkkkkkkkkkkkkkkkkk"


class SC_Employee_Ext(models.Model):
	_name = 'ext.employee'

	emp_filed = fields.Many2one('hr.employee')

	relation = fields.Text("Relation")
	name = fields.Char("Name")
	cnic = fields.Char("CNIC")	
	e_contact = fields.Char("Contact")
	per_address = fields.Text("Permanent Address")
	tem_address = fields.Text("Temporary Address")
	main = fields.Boolean("Main")
	








