from odoo import http
from odoo.http import request
import re
import json

class ClassController(http.Controller):
    @http.route('/api/class/create', type='http', auth='user', methods=['POST'], csrf=False)
    def create_class(self, **kwargs):
        try:
            # Cargar datos JSON manualmente
            data = json.loads(request.httprequest.data)

            # Recuperar datos
            name = data.get('name')
            code = data.get('code')
            section = data.get('section')
            hour = data.get('hour')
            year = data.get('year')
            period = data.get('period')
            docent_id = data.get('docent_id')
            student_ids = data.get('student_ids', [])
            active = data.get('active', True)

            # Validar campos obligatorios
            if not name or not code or not section or not year or not period or not docent_id:
                return request.make_response(
                    json.dumps({"error": "Faltan campos obligatorios: 'name', 'code', 'section', 'year', 'period', 'docent_id'."}),
                    headers=[('Content-Type', 'application/json')],
                )

            # Verificar duplicados
            existing_class = request.env['school.class'].sudo().search([
                ('code', '=', code),
                ('section', '=', section),
                ('hour', '=', hour),
                ('year', '=', year),
                ('period', '=', period)
            ], limit=1)

            if existing_class:
                return request.make_response(
                    json.dumps({"error": "Ya existe una clase con el mismo código, sección, horario, año y período."}),
                    headers=[('Content-Type', 'application/json')],
                )

            # Validar los IDs de estudiantes
            invalid_student_ids = []
            for student_id in student_ids:
                student = request.env['school.student'].sudo().browse(student_id)
                if not student.exists():
                    invalid_student_ids.append(student_id)

            if invalid_student_ids:
                return request.make_response(
                    json.dumps({"error": f"Los siguientes estudiantes no existen: {', '.join(map(str, invalid_student_ids))}"}),
                    headers=[('Content-Type', 'application/json')],
                )

            # Crear clase
            new_class = request.env['school.class'].sudo().create({
                'name': name,
                'code': code,
                'section': section,
                'hour': hour,
                'year': year,
                'period': period,
                'docent_id': docent_id,
                'student_ids': [(6, 0, student_ids)],  # Asignar estudiantes
                'active': active,
            })

            return request.make_response(
                json.dumps({"success": True, "class_id": new_class.id}),
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
