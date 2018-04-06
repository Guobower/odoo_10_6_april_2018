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



class hr_create_user_bio_machine_not_web(models.Model):
	_inherit = 'hr.employee'

	

	
	@api.multi
	def createBioUsers_not_web(self):
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
				zk = ZK(ip, port=4370, timeout=5)
				# connect = zk.connect()
				self._checkMachine(zk)
				connect = zk.connect()
				print "23333333333333333"
				connect.disable_device()
				print "444444444444444444444"
				users = connect.get_users()
				for user in users:
					# print user
					print str(self.emp_machine_id)
					print "xxxxxxxxxxxxxxxxxxxxxx"
					machine_id=user.user_id
					print machine_id
					if str(machine_id)==str(self.emp_machine_id):
						print "yyyyyyyyyyyyyyyyyyyyyyyyyyy"
						connect.enable_device()
						connect.disconnect()
						raise ValidationError('User Already Present In Machine')
				connect.set_user(uid=int(self.emp_machine_id), name=str(self.name), privilege=const.USER_DEFAULT, password='1', group_id='', user_id=str(self.emp_machine_id))
				# if connect:
				connect.enable_device()
				connect.disconnect()

 	def _checkMachine(self, machineInstance):
 		connect = None
 		try:
 			connect = machineInstance.connect()
 			print "22222222222222222222222222222"
 		except Exception, e:
 			raise ValidationError('Machine Not Active Please Fix It')

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
				connect = None
				zk = ZK(ip, port=4370, timeout=5)
				# self._checkMachine(zk)
				try:
					connect = zk.connect()
					connect.disable_device()
					users = connect.get_users()
					machine_id = []
					for user in users:
						machine_id.append(user.user_id)
					counter = 0
					for x in machine_id:
						if str(x) == str(self.emp_machine_id):
							counter = counter + 1

					if counter == 0:
						raise ValidationError('User Already Delete In Machine')

					connect.delete_user(int(self.emp_machine_id))
				
				except Exception, e:
					print "Process terminate not connnect ......... : {}".format(e)
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
				zk = ZK(ip, port=4370, timeout=5)
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
						print record['user_id']
						raw_attendence=self.env['struct.attend'].search([('attendance_date','=',record['Real_Timestamp']),('machine_id','=',record['user_id']),('name','=',ip)])
						if not raw_attendence:
							membership=self.env['reg.form'].search([('emp_machine_id','=',record['user_id'])])
							print "44444444444444444"


							self.env['struct.attend'].create({
											'employee_id': membership.id,
											'member_photo': membership.member_photo,
											# 'department': employee_id_raw.department_id.id,
											'attendance_date': record['Real_Timestamp'],
											'name': ip,
											'machine_id': record['user_id'],
											'date': real_date[0],
											'time': real_date[1],
											'branch': membership.branch.id,
											# 'time': (datetime.now() + timedelta(hours=5)).strftime("%H:%M:%S"),
											# 'machine_name': 'yasir',
									})

				except Exception, e:
					print "Process terminate not connnect ......... : {}".format(e)
				finally:
					if connect:
						connect.enable_device()
						connect.disconnect()
	
	@api.multi
	def clearAttendence(self):
		print "111111111111111111111111"
		self._updateAttendanceAll()
		print "2222222222222222222222"
		machine_list=self.env['machine.info'].search([])
		for x in machine_list.product_ids:
			if not x.status=="no":
				ip=x.ip
				connect = None
				zk = ZK(ip, port=4370, timeout=20)
				connect = zk.connect()
				connect.disable_device()
				clear_attende = connect.clear_attendance()
				connect.enable_device()
				connect.disconnect()



class hr_create_user_bio_machine_rejoing(models.Model):
	_inherit = 'struct.rejoining'	

	
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
		member_no=self.membership_no.memship_no
		for x in machine_list.product_ids:
			if not x.status=="no":
				ip=x.ip
				print ip
				connect = None
				zk = ZK(ip, port=4370, timeout=5)
				# connect = zk.connect()
				self._checkMachine(zk)
				connect = zk.connect()
				connect.disable_device()
				users = connect.get_users()
				for user in users:
					machine_id=user.user_id
					if str(machine_id)==str(member_no):
						connect.enable_device()
						connect.disconnect()
						raise ValidationError('User Already Present In Machine')
				connect.set_user(uid=int(member_no), name=str(self.member.name), privilege=const.USER_DEFAULT, password='1', group_id='', user_id=str(member_no))
				# if connect:
				connect.enable_device()
				connect.disconnect()

 	def _checkMachine(self, machineInstance):
 		connect = None
 		try:
 			connect = machineInstance.connect()
 			print "22222222222222222222222222222"
 		except Exception, e:
 			raise ValidationError('Machine Not Active Please Fix It')

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
		member_no=self.membership_no.memship_no
		for x in machine_list.product_ids:
			if not x.status=="no":
				ip=x.ip
				connect = None
				zk = ZK(ip, port=4370, timeout=2)
				self._checkMachine(zk)
				connect = zk.connect()
				connect.disable_device()
				users = connect.get_users()
				machine_id = []
				for user in users:
					machine_id.append(user.user_id)
				counter = 0
				for x in machine_id:
					if str(x) == str(member_no):
						counter = counter + 1

				if counter == 0:
					raise ValidationError('User Already Delete In Machine')

				connect.delete_user(int(member_no))
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