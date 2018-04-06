from odoo import models, fields, api
from datetime import datetime, timedelta

class hr_notification(models.Model):
    _name = 'hr.notification'

    def mail_remainder(self, cr, uid, context=None):
        next_day = datetime.now() + timedelta(days=1)
        hr_employee_obj_iqama = self.pool.get('hr.employee').search(cr, uid, [('iqama_date_of_expiry', '<=', next_day)])
        for rec in hr_employee_obj_iqama:
            self.send_email_iqama(cr, uid, rec, context)
        hr_employee_obj_passport = self.pool.get('hr.employee').search(cr, uid, [('passport_date_of_expiry', '<=', next_day)])
        for rec in hr_employee_obj_passport:
            self.send_email_passport(cr, uid, rec, context)

    def send_email_iqama(self, cr, uid, employee, context=None):
        email = self.pool.get('hr.employee').browse(cr, uid, employee).work_email
        email_template_obj = self.pool.get('email.template')
        template_ids = email_template_obj.search(cr, uid, [('name', '=', 'Iqama Expiration Alert')], context=context)
        email_template_obj.write(cr, uid, template_ids,{'email_to': email}, context)
        if template_ids:
            values = email_template_obj.generate_email(cr, uid, template_ids[0],employee, context=context)
            mail_mail_obj = self.pool.get('mail.mail')
            msg_id = mail_mail_obj.create(cr, uid, values, context=context)
            if msg_id:
                mail_mail_obj.send(cr, uid, [msg_id], context=context)
        return True

    def send_email_passport(self, cr, uid, employee, context=None):
        email = self.pool.get('hr.employee').browse(cr, uid, employee).work_email
        email_template_obj = self.pool.get('email.template')
        template_ids = email_template_obj.search(cr, uid, [('name', '=', 'Passport Expiration Alert')], context=context)
        email_template_obj.write(cr, uid, template_ids,{'email_to': email}, context)
        if template_ids:
            values = email_template_obj.generate_email(cr, uid, template_ids[0],employee, context=context)
            mail_mail_obj = self.pool.get('mail.mail')
            msg_id = mail_mail_obj.create(cr, uid, values, context=context)
            if msg_id:
                mail_mail_obj.send(cr, uid, [msg_id], context=context)
        return True