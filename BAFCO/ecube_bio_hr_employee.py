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

	emp_machin_id=fields.Char('Employee Id')
	
	@api.model
	def _Get_Attenndence_Selenium(self):
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
			# raw_attendence=self.env['ecube.raw.attendance'].search([('machine_id','=',list_id[index_id]),('machine_date','=',list_date[index_id]),('machine_time','=',list_time[index_id])])
			# if not raw_attendence:
			employee_id_raw =self.env['hr.employee'].search([('emp_machin_id','=',list_id[index_id])])
			print employee_id_raw
			self.env['ecube.raw.attendance'].create({
							'employee_id': employee_id_raw.id,
							'machine_id': list_id[index_id],
							'machine_date': list_date[index_id],
							# 'machine_time': list_time[index_id],
					})
		index_id = index_id +1
		if "%s/attlog.dat" % DIR_PATH:
			os.remove(DIR_PATH)
		# zk = zklib.ZKLib(config.key['ip'], int(config.key['port']))
		# res = zk.connect()
		display = Display(visible=0, size=(800, 600))
		display.start()

		# profile = webdriver.FirefoxProfile()
		# profile.set_preference("browser.download.panel.shown", False)
		# profile.set_preference("browser.helperApps.neverAsk.openFile","text/csv,application/vnd.ms-excel")
		# profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv,application/vnd.ms-excel,text/dat,text/plain")
		# profile.set_preference("browser.download.folderList", 2);
		# profile.set_preference("browser.download.dir", "/home/rocky/Downloads/")
		# chrome_options = Options()
		# chrome_options.add_argument("--headless")



		options = Options()
		options.add_experimental_option("prefs", {
		  "download.default_directory": r"/home/odoo/Downloads",
		  "download.prompt_for_download": False,
		  "download.directory_upgrade": True,
		  "safebrowsing.enabled": True
		})

		# browser = webdriver.Firefox(executable_path="/home/rocky/Downloads/geckodriver")
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
		time.sleep(5)
		print "username is typed"
		browser.find_element_by_xpath(xpaths['passwd']).clear()
		browser.find_element_by_xpath(xpaths['passwd']).send_keys('10403')
		time.sleep(5)
		print "password is typed"
		browser.find_element_by_xpath(xpaths['login']).click()
		browser.get('http://37.99.147.178:4370/csl/download')
		time.sleep(5)
		browser.find_element_by_xpath(xpaths['download']).click()
		# time.sleep(50)
		# browser.quit()
		print "browser Closed"
		# display.stop()
# /home/odoo/phantomjs/home/odoo/phantomjs

# Steps that required for this F*****G machine
# Install https://github.com/dnaextrim/python_zklib this library
# Install Selenium
# Download Gekodriver
# Export path of Geckodriver
# Install sudo apt-get install xvfb
#install sudo pip install pyvirtualdisplay