# -*- coding: utf-8 -*-
from odoo import http

# class Crowncity(http.Controller):
#     @http.route('/crowncity/crowncity/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/crowncity/crowncity/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('crowncity.listing', {
#             'root': '/crowncity/crowncity',
#             'objects': http.request.env['crowncity.crowncity'].search([]),
#         })

#     @http.route('/crowncity/crowncity/objects/<model("crowncity.crowncity"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('crowncity.object', {
#             'object': obj
#         })