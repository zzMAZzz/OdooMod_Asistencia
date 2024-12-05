from odoo import http
from odoo.http import request
import json

class DocentController(http.Controller):

    @http.route('/api/docent/create', type='http', auth='public', methods=['POST'], csrf=False)
    def create_docent(self, **kwargs):
        try:
            # Cargar datos JSON desde la solicitud
            data = json.loads(request.httprequest.data)

            # Recuperar los datos del JSON
            name = data.get('name')
            cuenta = data.get('cuenta')
            email = data.get('email')
            active = data.get('active', True)

            # Validar campos obligatorios
            if not name or not cuenta or not email:
                return request.make_response(
                    json.dumps({"error": "Faltan campos obligatorios: 'name', 'cuenta', 'email'."}),
                    headers=[('Content-Type', 'application/json')]
                )

            # Verificar si ya existe un docente con la misma cuenta
            existing_docent = request.env['school.docent'].sudo().search([('cuenta', '=', cuenta)], limit=1)
            if existing_docent:
                return request.make_response(
                    json.dumps({"error": "Ya existe un docente con este número de cuenta."}),
                    headers=[('Content-Type', 'application/json')]
                )

            # Crear el docente
            docent = request.env['school.docent'].sudo().create({
                'name': name,
                'cuenta': cuenta,
                'email': email,
                'active': active
            })

            return request.make_response(
                json.dumps({"success": True, "docent_id": docent.id}),
                headers=[('Content-Type', 'application/json')]
            )

        except json.JSONDecodeError:
            return request.make_response(
                json.dumps({"error": "Error al procesar los datos JSON."}),
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            return request.make_response(
                json.dumps({"error": str(e)}),
                headers=[('Content-Type', 'application/json')]
            )
