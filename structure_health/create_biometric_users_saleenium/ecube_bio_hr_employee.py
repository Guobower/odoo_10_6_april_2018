# -*- coding: utf-8 -*-
import os
import numpy as np
from zklib import zklib
from zklib import zkconst
from datetime import datetime , timedelta
import time 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options



from pyvirtualdisplay import Display
import xmlrpclib

from openerp import models, fields, api
from openerp.exceptions import Warning
from odoo.exceptions import UserError
from openerp.exceptions import UserError
import config


class hr_create_user_bio_machine(models.Model):
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
				self._checkMachine(zk)
				connect = zk.connect()
				connect.disable_device()
				member_Reocrd=self.env['']

				connect.set_user(uid=int(self.card_no.name), name=str(self.name), privilege=const.USER_DEFAULT, password='1', group_id='', user_id=str(self.card_no.name))
				connect.enable_device()
				connect.disconnect()


	@api.multi
	def createBioUsersall(self):
		zk = zklib.ZKLib(config.key['ip'], int(config.key['port']))
		res = zk.connect()
		if res == True:
			zk.enableDevice()
			zk.disableDevice()
				record=self.env['hr.employee'].search([])
				for r_list in record:
					for user in BioUsers[0]:
						if (BioUsers[0][user][0] == str(r_list.emp_machine_id)):
							pass
					zk.setUser(uid=False, userid=str(r_list.emp_machine_id), name=str(r_list.name), password='', role=zkconst.LEVEL_USER)

					zk.enableDevice()				
			else:
				for user in BioUsers[0]:
					if (BioUsers[0][user][0] == str(self.emp_machine_id)):
						raise Warning('User Already Present in Machine.')
				zk.setUser(uid=False, userid=str(self.emp_machine_id), name=str(self.name), password='', role=zkconst.LEVEL_USER)

				zk.enableDevice()
				
			zk.disconnect()
			zk.refreshData()


	@api.model
	def _Get_Attenndence_Selenium(self):
		display = Display(visible=0, size=(800, 600))
		display.start()
		options = Options()
		options.add_experimental_option("prefs", {
		  "download.default_directory": r"/home/odoo/Downloads",
		  "download.prompt_for_download": False,
		  "download.directory_upgrade": True,
		  "safebrowsing.enabled": True
		})

		browser = webdriver.Chrome(executable_path="/home/odoo/Downloads/chromedriver")
		browser.wait = WebDriverWait(browser, 5)
		browser.get('http://37.99.147.178:4370')
		xpaths = { 'username' :   "//input[@name='username']",
				   'passwd' : "//input[@name='userpwd']",
				   'login' : "//input[contains(@value,'Login')]",
				   'download' : "//input[contains(@value,'Download')]",
				   'search' : "//input[contains(@value,'Search')]",
				   'report' : "//a[text()='Report']"
				 }

		print "Browser is opened"

		browser.find_element_by_xpath(xpaths['username']).clear()
		browser.find_element_by_xpath(xpaths['username']).send_keys('10403')
		time.sleep(3)
		print "username is typed"
		browser.find_element_by_xpath(xpaths['passwd']).clear()
		browser.find_element_by_xpath(xpaths['passwd']).send_keys('10403')
		time.sleep(3)
		print "password is typed"
		browser.find_element_by_xpath(xpaths['login']).click()
		browser.get('http://37.99.147.178:4370/csl/download')
		time.sleep(3)
		browser.find_element_by_xpath(xpaths['download']).click()
		# time.sleep(50)
		# browser.quit()
		print "browser Closed"
		time.sleep(3)
		dir_path = os.path.dirname(os.path.realpath(__file__))
		DIR_PATH = '/home/odoo/Downloads'+'/attlog.dat'
		# DIR_PATH = '/home/odoo/'
		list_id=[]
		list_name=[]
		list_date=[]
		list_time=[]

		for line in open(DIR_PATH, 'r'):
			item = line.rstrip()
			words=item.replace('\t', ' ')
			w_list = words.split(" ")
			count_name=0
			count_id=0
			count_id_id =0
			count_date=0
			count =0
			for record in w_list:
				count = count + 1
				if count == 1:
					list_id.append(record)
				if count == 2:
					list_name.append(record)
				if count == 3:
					list_date.append(record)
				if count == 4:
					list_time.append(record)
		index_id=0
		for emp_id in list_id:
			print list_id[index_id]
			print list_date[index_id]
			print "search preveious Record "
			raw_attendence=self.env['ecube.raw.attendance'].search([('machine_id','=',list_id[index_id]),('machine_date','=',list_date[index_id]),('machine_time','=',list_time[index_id])])
			print "recored match"
			if not raw_attendence:
				employee_id_raw =self.env['hr.employee'].search([('emp_machin_id','=',list_id[index_id])])
				print employee_id_raw
				print "create record"
				self.env['ecube.raw.attendance'].create({
								'employee_name': employee_id_raw.id,
								'machine_id': list_id[index_id],
								'machine_date': list_date[index_id],
								'machine_time': list_time[index_id],
						})
			index_id = index_id +1
		if "%s/attlog.dat" % DIR_PATH:
			os.remove(DIR_PATH)
		# display.stop()
# /home/odoo/phantomjs/home/odoo/phantomjs

# Steps that required for this F*****G machine
# Install https://github.com/dnaextrim/python_zklib this library
# Install Selenium
# Download Gekodriver
# Export path of Geckodriver
# Install sudo apt-get install xvfb
#install sudo pip install pyvirtualdisplay