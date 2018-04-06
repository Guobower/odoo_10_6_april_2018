from openerp import models, api, fields, SUPERUSER_ID
from datetime import datetime, date
from openerp.exceptions import RedirectWarning


class hr_employee(models.Model):
    _inherit = "hr.employee"

    @api.one
    @api.depends('birthday')
    def compute_age(self):
        for emp in self:
            if emp.birthday:
                today = fields.date.today()
                born = datetime.strptime(emp.birthday, '%Y-%m-%d')
                self.age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    employee_type = fields.Selection([('direct', 'Direct Employee'), ('outsource_domestic', 'Outsourced Domestic'),
                                      ('outsource_commercial', 'Outsourced Commercial')],
                                     'Employee Type', required=False, track_visibility='onchange', index=True, )
    employee_grade = fields.Many2one('hr.employee.grade', 'Employee Grade')
    employee_status_id = fields.Many2one('hr.status', 'Status', required=False)
    religion_id = fields.Many2one('hr.religion', 'Religion', required=False)
    age = fields.Char('Age', compute='compute_age')
    place_of_birth = fields.Many2one('res.country', 'Country', ondelete='restrict')
    place_of_birth_city = fields.Char('City', translate=True, required=False)
    nationality = fields.Char('Nationality', translate=True, required=False)
    identification_id = fields.Char('ID', required=False)
    identification_type = fields.Selection([('iqama', 'Iqama'), ('national_id', 'National ID')],
                                           default='iqama', required=False)
    entry_number = fields.Char('Entry Number')
    iqama_date_of_issue = fields.Date('Date of Issue', required=False)
    iqama_date_of_expiry = fields.Date('Date of Expiry', required=False)
    # iqama_issuing_authority = fields.Char('Issuing Authority', translate=True, required=False)
    iqama_issuing_city = fields.Char('Issuing City', translate=True, required=False)
    sponsor_type = fields.Selection([('jihan', 'Jehan'), ('other', 'Other')], default='other', string='Sponsor Type')
    sponsor_id = fields.Char('Sponsor ID', translate=True, required=False)
    sponsor_name = fields.Char('Sponsor Name', translate=True, required=False)
    passport_issuing_authority = fields.Char('Issuing Authority', translate=True, required=False)
    passport_date_of_issue = fields.Date('Date of Issue', required=False)
    passport_date_of_expiry = fields.Date('Date of Expiry', required=False)
    joining_date = fields.Date('Joining Date', required=False)
    mobile_phone_2 = fields.Char('Mobile-2 No')
    educational_level_id = fields.Many2one('hr.education.level', 'Education Level', required=False)
    family_member_ids = fields.One2many('hr.family', 'employee_id', 'Family Details')
    insurance_ids = fields.One2many('hr.insurance', 'employee_id', 'Insurance Details')

    _defaults = {
        'employee_id': lambda obj, cr, uid, context: '/',
    }


class hr_status(models.Model):
    _name = 'hr.status'

    name = fields.Char('Name', required=True, translate=True)


class hr_employee_grade(models.Model):
    _name = 'hr.employee.grade'

    name = fields.Char('Name', required=True, translate=True)


class hr_religion(models.Model):
    _name = 'hr.religion'

    name = fields.Char('Name', required=True, translate=True)


class hr_education_level(models.Model):
    _name = 'hr.education.level'

    name = fields.Char('Name', required=True, translate=True)


class hr_insurance(models.Model):
    _name = 'hr.insurance'

    insurance_type_id = fields.Many2one('hr.insurance.type', 'Insurance Type')
    insurance_company_id = fields.Many2one('hr.insurance.company', 'Insurance Company')
    employee_id = fields.Many2one('hr.employee', ondelete='cascade')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')

class hr_insurance_type(models.Model):
    _name = 'hr.insurance.type'

    name = fields.Char('Name', required=True, translate=True)


class hr_insurance_company(models.Model):
    _name = 'hr.insurance.company'

    name = fields.Char('Name', required=True, translate=True)


