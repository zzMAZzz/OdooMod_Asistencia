from odoo import http
from odoo.http import request
import re
import json

class StudentController(http.Controller):
    @http.route('/api/student/create', type='http', auth='user', methods=['POST'], csrf=False)
    def create_student(self, **kwargs):
        try:
            # Cargar datos JSON manualmente
            data = json.loads(request.httprequest.data)

            # Recuperar datos
            name = data.get('name')
            cuenta = data.get('cuenta')
            email = data.get('email')
            age = data.get('age')
            gender = data.get('gender', 'male')

            # Validar campos obligatorios
            if not name or not cuenta or not email:
                return request.make_response(
                    json.dumps({"error": "Faltan campos obligatorios: 'name', 'cuenta', 'email'."}),
                    headers=[('Content-Type', 'application/json')],
                )

            # Validar tipo de datos
            if age and not isinstance(age, int):
                return request.make_response(
                    json.dumps({"error": "'age' debe ser un número entero."}),
                    headers=[('Content-Type', 'application/json')],
                )

            # Verificar duplicados
            existing_student = request.env['school.student'].sudo().search([ 
                '|',
                ('cuenta', '=', cuenta),
                ('email', '=', email)
            ], limit=1)

            if existing_student:
                return request.make_response(
                    json.dumps({"error": "Ya existe un estudiante con este número de cuenta o correo electrónico."}),
                    headers=[('Content-Type', 'application/json')],
                )

            # Crear estudiante
            student = request.env['school.student'].sudo().create({
                'name': name,
                'cuenta': cuenta,
                'email': email,
                'age': age,
                'gender': gender,
            })

            return request.make_response(
                json.dumps({"success": True, "student_id": student.id}),
                headers=[('Content-Type', 'application/json')],
            )

        except json.JSONDecodeError:
            return request.make_response(
                json.dumps({"error": "Error al procesar los datos JSON."}),
                headers=[('Content-Type', 'application/json')],
            )
        except Exception as e:
            return request.make_response(
                json.dumps({"error": str(e)}),
                headers=[('Content-Type', 'application/json')],
            )
        