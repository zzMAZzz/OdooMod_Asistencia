from odoo import http
from odoo.http import request
import json

class StudentController(http.Controller):

    # Crear un estudiante
    @http.route('/api/student/create', type='http', auth='user', methods=['POST'], csrf=False)
    def create_student(self, **kwargs):
        try:
            data = json.loads(request.httprequest.data)
            name = data.get('name')
            cuenta = data.get('cuenta')
            email = data.get('email')
            age = data.get('age')
            gender = data.get('gender', 'male')

            if not name or not cuenta or not email:
                return request.make_response(
                    json.dumps({"error": "Faltan campos obligatorios: 'name', 'cuenta', 'email'."}),
                    headers=[('Content-Type', 'application/json')],
                )

            if age and not isinstance(age, int):
                return request.make_response(
                    json.dumps({"error": "'age' debe ser un número entero."}),
                    headers=[('Content-Type', 'application/json')],
                )

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

    @http.route('/api/student/<int:student_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_student(self, student_id, **kwargs):
        try:
            student = request.env['school.student'].sudo().browse(student_id)
            if not student.exists():
                return request.make_response(
                    json.dumps({"error": "Estudiante no encontrado."}),
                    headers=[('Content-Type', 'application/json')],
                )

            student_data = {
                'id': student.id,
                'name': student.name,
                'cuenta': student.cuenta,
                'email': student.email,
                'age': student.age,
                'gender': student.gender,
            }

            return request.make_response(
                json.dumps({"student": student_data}),
                headers=[('Content-Type', 'application/json')],
            )

        except Exception as e:
            return request.make_response(
                json.dumps({"error": str(e)}),
                headers=[('Content-Type', 'application/json')],
            )

    @http.route('/api/student/update/<int:student_id>', type='http', auth='user', methods=['PUT'], csrf=False)
    def update_student(self, student_id, **kwargs):
        try:
            data = json.loads(request.httprequest.data)
            student = request.env['school.student'].sudo().browse(student_id)

            if not student.exists():
                return request.make_response(
                    json.dumps({"error": "Estudiante no encontrado."}),
                    headers=[('Content-Type', 'application/json')],
                )

            name = data.get('name')
            cuenta = data.get('cuenta')
            email = data.get('email')
            age = data.get('age')
            gender = data.get('gender', 'male')

            if name:
                student.name = name
            if cuenta:
                student.cuenta = cuenta
            if email:
                student.email = email
            if age:
                student.age = age
            if gender:
                student.gender = gender

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

    @http.route('/api/student/delete/<int:student_id>', type='http', auth='user', methods=['DELETE'], csrf=False)
    def delete_student(self, student_id, **kwargs):
        try:
            student = request.env['school.student'].sudo().browse(student_id)
            if not student.exists():
                return request.make_response(
                    json.dumps({"error": "Estudiante no encontrado."}),
                    headers=[('Content-Type', 'application/json')],
                )

            student.unlink()

            return request.make_response(
                json.dumps({"success": True, "message": "Estudiante eliminado."}),
                headers=[('Content-Type', 'application/json')],
            )

        except Exception as e:
            return request.make_response(
                json.dumps({"error": str(e)}),
                headers=[('Content-Type', 'application/json')],
            )
