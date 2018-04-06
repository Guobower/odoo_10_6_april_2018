# -*- coding: utf-8 -*-
from openerp import http
from openerp.http import request
from openerp.addons.web.controllers.main import serialize_exception,content_disposition
import base64
# import urllib
# from openerp import http

class DosSchedule(http.Controller):
    @http.route('/dos_schedule/dos_schedule/', auth='public')
    def index(self, **kw):
    	filename = "abc.txt"
    	# result =  urllib.urlretrieve(url, "Customer.xlsx")
    	filecontent = base64.b64decode(filename)
    	return request.make_response(filecontent,
    		[('Content-Type', 'application/octet-stream'),
    		('Content-Disposition', content_disposition(filename))])


# class DosSchedule(http.Controller):
#     @http.route('/dos_schedule/dos_schedule/', auth='public')
#     def index(self, **kw):
#         return "Hello World"
#     @http.route('/dos_schedule/dos_schedule/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dos_schedule.listing', {
#             'root': '/dos_schedule/dos_schedule',
#             'objects': http.request.env['dos_schedule.dos_schedule'].search([]),
#         })

#     @http.route('/dos_schedule/dos_schedule/objects/<model("dos_schedule.dos_schedule"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dos_schedule.object', {
#             'object': obj
#         })