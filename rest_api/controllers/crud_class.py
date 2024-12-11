from odoo import http
from odoo.http import request
import json

class ClassController(http.Controller):
    @http.route('/api/class/create', type='http', auth='user', methods=['POST'], csrf=False)
    def create_class(self, **kwargs):
        try:
            data = json.loads(request.httprequest.data)
            name = data.get('name')
            code = data.get('code')
            section = data.get('section')
            hour = data.get('hour')
            year = data.get('year')
            period = data.get('period')
            docent_id = data.get('docent_id')
            student_ids = data.get('student_ids', [])
            active = data.get('active', True)

            # Asegurarse de que los campos obligatorios están presentes
            if not name or not code or not section or not year or not period or not docent_id:
                return request.make_response(
                    json.dumps({"error": "Faltan campos obligatorios: 'name', 'code', 'section', 'year', 'period', 'docent_id'."}),
                    headers=[('Content-Type', 'application/json')],
                )

            # Convertir year y hour a enteros si son cadenas
            year = int(year) if isinstance(year, str) else year
            hour = int(hour) if isinstance(hour, str) else hour
            docent_id = int(docent_id) if isinstance(docent_id, str) else docent_id

            # Verificar si ya existe la clase con los mismos parámetros
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

            new_class = request.env['school.class'].sudo().create({
                'name': name,
                'code': code,
                'section': section,
                'hour': hour,
                'year': year,
                'period': period,
                'docent_id': docent_id,
                'student_ids': [(6, 0, student_ids)],
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

    @http.route('/api/class/<int:class_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_class(self, class_id, **kwargs):
        try:
            class_record = request.env['school.class'].sudo().browse(class_id)

            if not class_record.exists():
                return request.make_response(
                    json.dumps({"error": "Clase no encontrada."}),
                    headers=[('Content-Type', 'application/json')],
                )

            class_data = {
                'id': class_record.id,
                'name': class_record.name,
                'code': class_record.code,
                'section': class_record.section,
                'hour': class_record.hour,
                'year': class_record.year,
                'period': class_record.period,
                'docent_id': class_record.docent_id.id,
                'student_ids': [student.id for student in class_record.student_ids],
                'active': class_record.active,
            }

            return request.make_response(
                json.dumps({"class": class_data}),
                headers=[('Content-Type', 'application/json')],
            )

        except Exception as e:
            return request.make_response(
                json.dumps({"error": str(e)}),
                headers=[('Content-Type', 'application/json')],
            )

    @http.route('/api/class/update/<int:class_id>', type='http', auth='user', methods=['PUT'], csrf=False)
    def update_class(self, class_id, **kwargs):
        try:
            data = json.loads(request.httprequest.data)
            class_record = request.env['school.class'].sudo().browse(class_id)

            if not class_record.exists():
                return request.make_response(
                    json.dumps({"error": "Clase no encontrada."}),
                    headers=[('Content-Type', 'application/json')],
                )

            name = data.get('name')
            code = data.get('code')
            section = data.get('section')
            hour = data.get('hour')
            year = data.get('year')
            period = data.get('period')
            docent_id = data.get('docent_id')
            student_ids = data.get('student_ids', [])
            active = data.get('active')

            if year:
                year = int(year) if isinstance(year, str) else year
            if hour:
                hour = int(hour) if isinstance(hour, str) else hour
            if docent_id:
                docent_id = int(docent_id) if isinstance(docent_id, str) else docent_id

            if name:
                class_record.name = name
            if code:
                class_record.code = code
            if section:
                class_record.section = section
            if hour:
                class_record.hour = hour
            if year:
                class_record.year = year
            if period:
                class_record.period = period
            if docent_id:
                class_record.docent_id = docent_id
            if student_ids is not None:
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
                class_record.student_ids = [(6, 0, student_ids)]

            if active is not None:
                class_record.active = active

            return request.make_response(
                json.dumps({"success": True, "class_id": class_record.id}),
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

    @http.route('/api/class/delete/<int:class_id>', type='http', auth='user', methods=['DELETE'], csrf=False)
    def delete_class(self, class_id, **kwargs):
        try:
            # Intentar eliminar directamente sin mucha lógica adicional
            class_record = request.env['school.class'].sudo().browse(class_id)
            if not class_record.exists():
                return request.make_response(
                    json.dumps({"error": "Clase no encontrada."}),
                    headers=[('Content-Type', 'application/json')],
                )

            class_record.unlink()  # Eliminar la clase directamente
            return request.make_response(
                json.dumps({"success": True, "message": "Clase eliminada."}),
                headers=[('Content-Type', 'application/json')],
            )
        except Exception as e:
            return request.make_response(
                json.dumps({"error": str(e)}),
                headers=[('Content-Type', 'application/json')],
            )
