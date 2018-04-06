# -*- coding: utf-8 -*-
import xmlrpclib
from openerp import models, fields, api
from openerp.exceptions import Warning
from openerp.exceptions import ValidationError
from openerp.exceptions import UserError
import config
import os
from zk import ZK, const
import time
import datetime
from datetime import date, datetime, timedelta


class hr_create_user_bio_machine(models.Model):
	_inherit = 'reg.form'

	_sql_constraints= [('emp_machine_id','unique(emp_machine_id)','this MAchine ID IS already Exist')]
	

	
	@api.multi
	def createBioUsers(self):
		machine_list=self.env['machine.info'].search([])
		if not machine_list:
			machine_list=self.env['machine.info'].create({
				'db' : 'data base',
				})
		data_base=machine_list.db
		print data_base
		login=machine_list.odooLogin
		print login
		odoopwd=machine_list.odooPasswd
		print odoopwd
		ip_list=[]
		for x in machine_list.product_ids:
			if not x.status=="no":
				ip=x.ip
				print ip
				connect = None
				zk = ZK(ip, port=4370, timeout=2)
				connect = zk.connect()
				try:
					connect.disable_device()
					users = connect.get_users()
					print self.emp_machine_id
					print "111111111"
					for user in users:
						machine_id=user.user_id
						print machine_id
						if machine_id==str(self.emp_machine_id):
							raise ValidationError('User Already Present In Machine')
					connect.set_user(uid=int(self.emp_machine_id), name=str(self.name), privilege=const.USER_DEFAULT, password='1', group_id='', user_id=str(self.emp_machine_id))

				except Exception, e:
					print "Process terminate : {}".format(e)
				finally:
					if connect:
						connect.enable_device()
						connect.disconnect()
	

	@api.multi
	def deleteBioUsers(self):
		machine_list=self.env['machine.info'].search([])
		if not machine_list:
			machine_list=self.env['machine.info'].create({
				'db' : 'data base',
				})
		data_base=machine_list.db
		print data_base
		login=machine_list.odooLogin
		print login
		odoopwd=machine_list.odooPasswd
		print odoopwd
		ip_list=[]
		for x in machine_list.product_ids:
			if not x.status=="no":
				ip=x.ip
				print ip
				connect = None
				zk = ZK(ip, port=4370, timeout=2)
				try:
					connect = zk.connect()
					connect.disable_device()
					users = connect.get_users()
					print "333333333333333333"
					machine_id = []
					for user in users:
						machine_id.append(user.user_id)
					counter = 0
					for x in machine_id:
						print x
						if str(x) == str(self.emp_machine_id):
							counter = counter + 1

					if counter == 0:
						raise ValidationError('User Already Delete In Machine')

					print "ooooooooooooooooooo"
					connect.delete_user(int(self.emp_machine_id))
				except Exception, e:
					print "Process terminate : {}".format(e)
				finally:
					if connect:
						connect.enable_device()
						connect.disconnect()


	@api.multi
	def _updateAttendanceAll(self):
		machine_list=self.env['machine.info'].search([])
		if not machine_list:
			machine_list=self.env['machine.info'].create({
				'db' : 'data base',
				})
		data_base=machine_list.db
		print data_base
		login=machine_list.odooLogin
		print login
		odoopwd=machine_list.odooPasswd
		print odoopwd
		ip_list=[]
		for x in machine_list.product_ids:
			if not x.status=="no":
				ip=x.ip
				print ip
				connect = None
				zk = ZK('192.168.100.201', port=4370, timeout=2)
				try:
					connect = zk.connect()
					connect.disable_device()
					attendances = connect.get_attendance()
					info = []
					for attendance in attendances:
						data = {
						'user_id' :attendance.user_id,
						'Timestamp' : str(attendance.timestamp - timedelta(minutes=300)),
						'Real_Timestamp' : str(attendance.timestamp),
						'Status' : attendance.status
						}
						info.append(data)	
					
					print info
					print ",,,,,,,,,,,,,,,,,,,,,,,,"
					users = connect.get_users()
					for record in info:
						print "222222222222222222"
						real_date=record['Real_Timestamp'].split(' ')
						today_date= date.today()
						print real_date[0]
						print today_date
						# if real_date[0]==today_date:
						print "33333333333333333333333333"
						raw_attendence=self.env['ecube.raw.attendance'].search([('attendance_date','=',record['Real_Timestamp']),('machine_id','=',record['user_id']),('name','=',ip)])
						if not raw_attendence:
							print "44444444444444444"

							self.env['ecube.raw.attendance'].create({
											# 'employee_id': employee_id_raw.id,
											# 'department': employee_id_raw.department_id.id,
											'attendance_date': record['Real_Timestamp'],
											'name': ip,
											'machine_id': record['user_id'],
											'date': real_date[0],
											'time': real_date[1],
											# 'time': (datetime.now() + timedelta(hours=5)).strftime("%H:%M:%S"),
											# 'machine_name': 'yasir',
									})
				except Exception, e:
					print "Process terminate : {}".format(e)
				finally:
					if connect:
						connect.enable_device()
						connect.disconnect()
# Steps that required for this F*****G machine
# Install https://github.com/dnaextrim/python_zklib this library
# Install Selenium
# Download Gekodriver
# Export path of Geckodriver
# Install sudo apt-get install xvfb
#install sudo pip install pyvirtualdisplay

# sudo apt-get install python-pip
# sudo pip install git+https://github.com/ehtishamfaisal/zklib.git
# sudo pip install pyvirtualdisplay
# sudo pip install selenium
# sudo apt-get install xvfb