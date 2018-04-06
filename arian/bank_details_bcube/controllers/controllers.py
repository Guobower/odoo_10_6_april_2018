# -*- coding: utf-8 -*-
from odoo import http

# class BankDetailsBcube(http.Controller):
#     @http.route('/bank_details_bcube/bank_details_bcube/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bank_details_bcube/bank_details_bcube/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bank_details_bcube.listing', {
#             'root': '/bank_details_bcube/bank_details_bcube',
#             'objects': http.request.env['bank_details_bcube.bank_details_bcube'].search([]),
#         })

#     @http.route('/bank_details_bcube/bank_details_bcube/objects/<model("bank_details_bcube.bank_details_bcube"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bank_details_bcube.object', {
#             'object': obj
#         })