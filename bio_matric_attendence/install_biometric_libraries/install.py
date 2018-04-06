import os
import config
from openerp import models, fields, api

class hr_install_bio_machine_lib(models.Model):
	_inherit = 'res.users'
	
	@api.model
	def install(self):
		""" when module insatll run terminal command in it"""
		os.system('sudo apt-get update')
		sudoPassword = config.key['machineSudoPwd']

		pip = 'sudo apt-get install python-pip -y'
		install_pip = os.system('echo %s| sudo -S %s' % (sudoPassword, pip))
		zklib = 'sudo pip install git+https://github.com/ehtishamfaisal/zklib.git'
		p = os.system('echo %s| sudo -S %s' % (sudoPassword, zklib))
		print "zklib finshedddddddd"