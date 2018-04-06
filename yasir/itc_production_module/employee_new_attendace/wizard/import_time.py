from openerp import models, fields, api
import xlrd
from datetime import datetime
from openerp.tools.translate import _


class ImportTime(models.TransientModel):
    _name = 'import.time.wiz'

    path_url = fields.Text(string='Path URL', required=True)

    @api.multi
    def import_time(self):
        try:
            xl_workbook = xlrd.open_workbook(self.path_url)
            xl_sheet = xl_workbook.sheet_by_index(0)
            for row_idx in range(0, xl_sheet.nrows):
                cell_obj1 = xl_sheet.cell(row_idx, 0)
                cell_obj2 = xl_sheet.cell(row_idx, 1)
                py_date = xlrd.xldate.xldate_as_datetime(cell_obj2.value, xl_workbook.datemode)
                py_date = datetime.strptime(str(py_date), '%Y-%m-%d %H:%M:%S')
                self.env['dummy.attendance'].create({
                    'employee_int': cell_obj1.value,
                    'date': py_date,
                })
        except:
            raise Warning(_('Warning!'),
                          _("Please check the path of the file!!"))


ImportTime()
