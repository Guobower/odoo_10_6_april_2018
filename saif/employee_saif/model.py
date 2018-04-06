# -*- coding: utf-8 -*- 
import psycopg2
import os


from odoo import models, fields, api

class MB_Project_Extension(models.Model):
	_inherit = 'hr.employee'

	f_name = fields.Char("Father Name")
	cnic = fields.Char("CNIC")
	religion = fields.Char("Religion")
	doj = fields.Date("D.O.J")
	e_contact = fields.Char("Contact")
	per_address = fields.Text("Permanent Address")
	tem_address = fields.Text("Temporary Address")
	emp_link = fields.One2many('ext.employee','emp_filed')


	@api.multi
	def call(self):	
		sudoPassword = '8653'
		command = 'asterisk -rvvvx "\originate SIP/205 extension 207@users\"'
		os.system('echo %s|sudo -S %s' % (sudoPassword, command))


	@api.multi
	def data_base(self):
		try:
			conn = psycopg2.connect("dbname='champion_db' user='postgres' host='localhost' password='odoo'")
		except:
			print "I am unable to connect to the database"
		cur = conn.cursor()
		cur.execute(""" SELECT * FROM account_invoice""")
		# cur.execute("SELECT tables FROM information_schema.tables WHERE table_type = 'BASE TABLE'AND table_schema NOT IN ('pg_catalog', 'information_schema')")
		result1 = cur.fetchall()
		# p = []
		# for x in result1:
		# 	# p.append(x[2])
		# 	print type(x)
		# 	print type(x[0])
		# 	print "222222222222222222222222222222222222222222222"
		# 	return 0
		# print type(p)	
		# print p 
		# for x in p:
		cr = self.env.cr
		# cr.execute(" INSERT INTO  (id,create_date,journal_id,partner_id,company_id,account_id,reference_type,currency_id,type) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(x[0],x[3],5,1,x[16],1,x[26],x[37],'out_invoice'))
		cr.execute("INSERT INTO  account_invoice (SELECT * FROM   dblink('dbname=champion_db','SELECT * FROM account_invoice'))")


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
	








