# -*- coding: utf-8 -*-
# from odoo import http


# class OmHospital(http.Controller):
#     @http.route('/demo_odoo15/demo_odoo15/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/demo_odoo15/demo_odoo15/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('demo_odoo15.listing', {
#             'root': '/demo_odoo15/demo_odoo15',
#             'objects': http.request.env['demo_odoo15.demo_odoo15'].search([]),
#         })

#     @http.route('/demo_odoo15/demo_odoo15/objects/<model("demo_odoo15.demo_odoo15"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('demo_odoo15.object', {
#             'object': obj
#         })
