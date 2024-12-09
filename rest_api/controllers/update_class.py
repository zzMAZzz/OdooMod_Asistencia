from odoo import http
from odoo.http import request
import json

class ClassController(http.Controller):

    @http.route('/api/class/update/students', type='http', auth='user', methods=['POST'], csrf=False)
    def update_class_students(self, **kwargs):
        try:
            # Cargar datos JSON desde la solicitud
            data = json.loads(request.httprequest.data)

            # Recuperar datos
            class_id = data.get('class_id')
            student_accounts = data.get('student_accounts', [])  # Lista de cuentas de estudiantes
            active = data.get('active', True)

            # Validar campos obligatorios
            if not class_id:
                return request.make_response(
                    json.dumps({"error": "Falta el campo obligatorio 'class_id'."}),
                    headers=[('Content-Type', 'application/json')]
                )

            # Buscar la clase
            class_record = request.env['school.class'].sudo().browse(class_id)
            if not class_record.exists():
                return request.make_response(
                    json.dumps({"error": "No existe una clase con el ID proporcionado."}),
                    headers=[('Content-Type', 'application/json')]
                )

            # Buscar los estudiantes por cuentas
            student_ids = []
            for account in student_accounts:
                student = request.env['school.student'].sudo().search([('cuenta', '=', account)], limit=1)
                if student.exists():
                    student_ids.append(student.id)
                else:
                    return request.make_response(
                        json.dumps({"error": f"El estudiante con cuenta {account} no existe."}),
                        headers=[('Content-Type', 'application/json')]
                    )

            # Actualizar la clase con los nuevos estudiantes
            class_record.write({
                'student_ids': [(6, 0, student_ids)],  # Asignar estudiantes por IDs
                'active': active
            })

            return request.make_response(
                json.dumps({"success": True, "class_id": class_record.id}),
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
