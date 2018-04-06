# -*- coding: utf-8 -*-
from odoo import http

# class CsvWriter(http.Controller):
#     @http.route('/csv_writer/csv_writer/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/csv_writer/csv_writer/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('csv_writer.listing', {
#             'root': '/csv_writer/csv_writer',
#             'objects': http.request.env['csv_writer.csv_writer'].search([]),
#         })

#     @http.route('/csv_writer/csv_writer/objects/<model("csv_writer.csv_writer"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('csv_writer.object', {
#             'object': obj
#         })