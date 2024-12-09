from odoo import http
from odoo.http import request
import json

class GetData(http.Controller):
    ## Generate QR
    @http.route('/generate_qr', type='json', auth='public', website=False, csrf=False, methods=['GET','POST'])
    def generate(self, **kw):
        return "QR Generado. OK."
    
    @http.route('/api/class/<int:class_id>/students', type='http', auth='public', methods=['GET'], csrf=False)
    def get_class_students(self, class_id, **kwargs):
        try:
            # Buscar la clase por ID
            school_class = request.env['school.class'].sudo().browse(class_id)
            
            if not school_class:
                return request.make_response(
                    json.dumps({"error": "Clase no encontrada."}),
                    headers=[('Content-Type', 'application/json')],
                )
            
            # Obtener los estudiantes matriculados en la clase
            students = school_class.student_ids
            
            # Preparar los datos de los estudiantes
            student_data = []
            for student in students:
                student_data.append({
                    'id': student.id,
                    'name': student.name,
                    'email': student.email,
                    'age': student.age,
                    'gender': student.gender,
                })
            
            # Devolver los datos en formato JSON
            return request.make_response(
                json.dumps({"students": student_data}),
                headers=[('Content-Type', 'application/json')],
            )
        except Exception as e:
            return request.make_response(
                json.dumps({"error": f"Error: {str(e)}"}),
                headers=[('Content-Type', 'application/json')],
            )