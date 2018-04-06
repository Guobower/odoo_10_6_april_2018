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
			if not x.status=="no" and x.status_web=="not_web":
				ip=x.ip
				print ip
				connect = None
				zk = ZK(ip, port=4370, timeout=5)
				self._checkMachine(zk)
				connect = zk.connect()
				connect.disable_device()
				users = connect.get_users()
				for user in users:
					machine_id=user.user_id
					if not str(machine_id)==str(self.card_no.name):
						continue
				connect.set_user(uid=int(self.card_no.name), name=str(self.name), privilege=const.USER_DEFAULT, password='1', group_id='', user_id=str(self.card_no.name))
				connect.enable_device()
				connect.disconnect()

 	def _checkMachine(self, machineInstance):
 		connect = None
 		try:
 			connect = machineInstance.connect()
 		except Exception, e:
 			raise ValidationError('Machine Not Active Please Fix It')

	# @api.multi
	# def deleteBioUsers(self):
	# 	machine_list=self.env['machine.info'].search([])
	# 	if not machine_list:
	# 		machine_list=self.env['machine.info'].create({
	# 			'db' : 'data base',
	# 			})
	# 	data_base=machine_list.db
	# 	print data_base
	# 	login=machine_list.odooLogin
	# 	print login
	# 	odoopwd=machine_list.odooPasswd
	# 	print odoopwd
	# 	ip_list=[]
	# 	for x in machine_list.product_ids:
	# 		if not x.status=="no":
	# 			ip=x.ip
	# 			connect = None
	# 			zk = ZK(ip, port=4370, timeout=5)
	# 			# self._checkMachine(zk)
	# 			try:
	# 				connect = zk.connect()
	# 				connect.disable_device()
	# 				users = connect.get_users()
	# 				machine_id = []
	# 				for user in users:
	# 					machine_id.append(user.user_id)
	# 				counter = 0
	# 				for x in machine_id:
	# 					if str(x) == str(self.emp_machine_id):
	# 						counter = counter + 1

	# 				if counter == 0:
	# 					raise ValidationError('User Already Delete In Machine')

	# 				connect.delete_user(int(self.emp_machine_id))
				
	# 			except Exception, e:
	# 				print "Process terminate not connnect ......... : {}".format(e)
	# 			finally:
	# 				if connect:
	# 					connect.enable_device()
	# 					connect.disconnect()


	@api.multi
	def _updateAttendanceAll_not_web(self):
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
			if not x.status=="no" and x.status_web=="not_web":
				ip=x.ip
				print ip
				connect = None
				zk = ZK(ip, port=4370, timeout=10)
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
					users = connect.get_users()
					for record in info:
						real_date=record['Real_Timestamp'].split(' ')
						today_date= date.today()
						user_id_name=record['user_id']
						machine_date=record['Real_Timestamp']
						employee_id_raw =self.env['hr.employee'].search([('card_no','=',user_id_name)])
						raw_attendence=self.env['ecube.raw.attendance'].search([('employee_id','=',employee_id_raw.id),('attendance_date','=',machine_date),('machine_id','=',user_id_name),('name','=',ip),('department','=',employee_id_raw.department_id.id)])
						if not raw_attendence:


							self.env['ecube.raw.attendance'].create({
											'employee_id': employee_id_raw.id,
											'department': employee_id_raw.department_id.id,
											'attendance_date': machine_date,
											'name': ip,
											'machine_id': str(user_id_name),
											'date': real_date[0],
											'time': real_date[1],
									})

				except Exception, e:
					print "Process terminate not connnect ......... : {}".format(e)
				finally:
					if connect:
						connect.enable_device()
						connect.disconnect()
	
	@api.multi
	def clearAttendence_not_web(self):
		print "111111111111111111111111"
		self._updateAttendanceAll_not_web()
		print "2222222222222222222222"
		machine_list=self.env['machine.info'].search([])
		for x in machine_list.product_ids:
			if not x.status=="no" and x.status_web=="not_web":
				ip=x.ip
				connect = None
				zk = ZK(ip, port=4370, timeout=10)
				connect = zk.connect()
				connect.disable_device()
				clear_attende = connect.clear_attendance()
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