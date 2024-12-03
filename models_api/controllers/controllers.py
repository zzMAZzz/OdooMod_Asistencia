# -*- coding: utf-8 -*-
# from odoo import http


# class ModelsApi(http.Controller):
#     @http.route('/models_api/models_api', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/models_api/models_api/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('models_api.listing', {
#             'root': '/models_api/models_api',
#             'objects': http.request.env['models_api.models_api'].search([]),
#         })

#     @http.route('/models_api/models_api/objects/<model("models_api.models_api"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('models_api.object', {
#             'object': obj
#         })

