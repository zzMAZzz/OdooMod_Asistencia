# -*- coding: utf-8 -*-
# from odoo import http


# class Asistencia(http.Controller):
#     @http.route('/asistencia/asistencia', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/asistencia/asistencia/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('asistencia.listing', {
#             'root': '/asistencia/asistencia',
#             'objects': http.request.env['asistencia.asistencia'].search([]),
#         })

#     @http.route('/asistencia/asistencia/objects/<model("asistencia.asistencia"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('asistencia.object', {
#             'object': obj
#         })

