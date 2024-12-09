from odoo import http
from odoo.http import request, Response
from io import BytesIO
import pandas as pd
import json
import logging

_logger = logging.getLogger(__name__)

class FileUploadController(http.Controller):
    @http.route('/upload/class_students', type='http', auth='user', methods=['POST'], csrf=False)
    def upload_class_students(self, **kwargs):
        try:
            # Verificar que el archivo esté presente
            if 'xlsx' not in kwargs or 'class_id' not in kwargs:
                return Response(
                    json.dumps({"status": "error", "message": "No se proporcionó un archivo Excel o el ID de la clase."}), 
                    content_type='application/json', 
                    status=400
                )

            # Verificar el formato del archivo
            file = kwargs['xlsx']
            if not file.filename.endswith(('.xlsx', '.xls')):
                return Response(
                    json.dumps({"status": "error", "message": "Formato no válido. Solo se aceptan archivos .xlsx o .xls"}), 
                    content_type='application/json', 
                    status=400
                )

            # Leer el archivo Excel
            excel_data = pd.read_excel(BytesIO(file.read()))
            _logger.info(f"Archivo recibido: {file.filename}. Contenido: {excel_data.head()}")

            # Obtener la clase
            class_id = int(kwargs['class_id'])
            school_class = request.env['school.class'].sudo().browse(class_id)
            if not school_class.exists():
                return Response(
                    json.dumps({"status": "error", "message": f"No existe una clase con el ID {class_id}."}),
                    content_type='application/json',
                    status=404
                )

            # Contadores para estadísticas
            created_count = 0
            updated_count = 0

            # Mapeo de valores de género
            gender_mapping = {
                'M': 'male',
                'F': 'female'
            }

            # Procesar cada fila del archivo
            for _, row in excel_data.iterrows():
                email = row['Email']
                gender = gender_mapping.get(row.get('Genero', 'M'), 'male')  # Convertir 'M' o 'F' a 'male' o 'female'

                student = request.env['school.student'].sudo().search([('email', '=', email)], limit=1)

                if student:
                    # Si el estudiante ya existe, actualizar sus datos y asociarlo con la clase
                    student.write({
                        'name': row['Nombre'],
                        'age': row.get('Edad', student.age),
                        'gender': gender,  # Usar el género mapeado
                    })
                    if student.id not in school_class.student_ids.ids:
                        school_class.write({'student_ids': [(4, student.id)]})  # Añadir estudiante a la clase
                    updated_count += 1
                else:
                    # Crear un nuevo estudiante y asociarlo con la clase
                    new_student = request.env['school.student'].sudo().create({
                        'cuenta': row['Cuenta'],
                        'name': row['Nombre'],
                        'email': email,
                        'age': row.get('Edad', 0),
                        'gender': gender,  # Usar el género mapeado
                    })
                    school_class.write({'student_ids': [(4, new_student.id)]})  # Añadir estudiante a la clase
                    created_count += 1

            # Respuesta exitosa con estadísticas
            return Response(
                json.dumps({
                    "status": "success",
                    "message": "Archivo procesado exitosamente.",
                    "created": created_count,
                    "updated": updated_count,
                }),
                content_type='application/json',
                status=200
            )
        except Exception as e:
            _logger.error(f"Error al procesar el archivo: {str(e)}", exc_info=True)
            return Response(
                json.dumps({"status": "error", "message": f"Error procesando el archivo: {str(e)}"}), 
                content_type='application/json', 
                status=500
            )