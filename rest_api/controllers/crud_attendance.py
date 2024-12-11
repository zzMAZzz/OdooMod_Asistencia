from odoo import http
from odoo.http import request
import json

class AttendanceController(http.Controller):

    # Crear asistencia
    @http.route('/api/attendance/create', type='http', auth='public', methods=['POST'], csrf=False)
    def create_attendance(self, **kwargs):
        try:
            # Cargar datos JSON desde la solicitud
            data = json.loads(request.httprequest.data)

            # Recuperar los datos del JSON
            date = data.get('date')
            class_id = data.get('class_id')
            student_id = data.get('student_id')
            status = data.get('status', 'present')

            # Validar campos obligatorios
            if not date or not class_id or not student_id or not status:
                return request.make_response(
                    json.dumps({"error": "Faltan campos obligatorios: 'date', 'class_id', 'student_id', 'status'."}),
                    headers=[('Content-Type', 'application/json')]
                )

            # Verificar si ya existe un registro de asistencia para el estudiante en esa fecha
            existing_attendance = request.env['school.attendance'].sudo().search([
                ('date', '=', date),
                ('class_id', '=', class_id),
                ('student_id', '=', student_id)
            ], limit=1)
            
            if existing_attendance:
                return request.make_response(
                    json.dumps({"error": "Ya existe un registro de asistencia para este estudiante en esta fecha."}),
                    headers=[('Content-Type', 'application/json')]
                )

            # Crear el registro de asistencia
            attendance = request.env['school.attendance'].sudo().create({
                'date': date,
                'class_id': class_id,
                'student_id': student_id,
                'status': status
            })

            return request.make_response(
                json.dumps({"success": True, "attendance_id": attendance.id}),
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

    # Leer asistencia
    @http.route('/api/attendance/<int:attendance_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_attendance(self, attendance_id, **kwargs):
        try:
            # Buscar el registro de asistencia por ID
            attendance = request.env['school.attendance'].sudo().browse(attendance_id)

            if not attendance.exists():
                return request.make_response(
                    json.dumps({"error": "Registro de asistencia no encontrado."}),
                    headers=[('Content-Type', 'application/json')]
                )

            # Convertir la fecha a formato string
            attendance_date = attendance.date.strftime('%Y-%m-%d') if attendance.date else None

            # Preparar los datos de la respuesta
            attendance_data = {
                'id': attendance.id,
                'date': attendance_date,
                'class_id': attendance.class_id.id,
                'student_id': attendance.student_id.id,
                'status': attendance.status,
            }

            return request.make_response(
                json.dumps({"attendance": attendance_data}),
                headers=[('Content-Type', 'application/json')]
            )

        except Exception as e:
            return request.make_response(
                json.dumps({"error": str(e)}),
                headers=[('Content-Type', 'application/json')]
            )

    # Actualizar asistencia
    @http.route('/api/attendance/update/<int:attendance_id>', type='http', auth='public', methods=['PUT'], csrf=False)
    def update_attendance(self, attendance_id, **kwargs):
        try:
            # Cargar datos JSON desde la solicitud
            data = json.loads(request.httprequest.data)

            # Buscar el registro de asistencia por ID
            attendance = request.env['school.attendance'].sudo().browse(attendance_id)

            if not attendance.exists():
                return request.make_response(
                    json.dumps({"error": "Registro de asistencia no encontrado."}),
                    headers=[('Content-Type', 'application/json')]
                )

            # Actualizar los campos de la asistencia
            date = data.get('date', attendance.date)
            class_id = data.get('class_id', attendance.class_id.id)
            student_id = data.get('student_id', attendance.student_id.id)
            status = data.get('status', attendance.status)

            # Actualizar el registro
            attendance.write({
                'date': date,
                'class_id': class_id,
                'student_id': student_id,
                'status': status
            })

            return request.make_response(
                json.dumps({"success": True, "attendance_id": attendance.id}),
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

    # Eliminar asistencia
    @http.route('/api/attendance/delete/<int:attendance_id>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def delete_attendance(self, attendance_id, **kwargs):
        try:
            # Buscar el registro de asistencia por ID
            attendance = request.env['school.attendance'].sudo().browse(attendance_id)

            if not attendance.exists():
                return request.make_response(
                    json.dumps({"error": "Registro de asistencia no encontrado."}),
                    headers=[('Content-Type', 'application/json')]
                )

            # Eliminar el registro de asistencia
            attendance.unlink()

            return request.make_response(
                json.dumps({"success": True}),
                headers=[('Content-Type', 'application/json')]
            )

        except Exception as e:
            return request.make_response(
                json.dumps({"error": str(e)}),
                headers=[('Content-Type', 'application/json')]
            )
