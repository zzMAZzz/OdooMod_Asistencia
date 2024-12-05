from odoo import http
from odoo.http import request, Response
from io import BytesIO
import pandas as pd
import json
import logging

_logger = logging.getLogger(__name__)

class FileUploadController(http.Controller):
    @http.route('/upload/excel', type='http', auth='public', methods=['POST'], csrf=False)
    def upload_excel(self, **kwargs):
        try:
            # Verificar que el archivo esté presente
            if 'xlsx' not in kwargs:
                return Response(
                    json.dumps({"status": "error", "message": "No se proporcionó un archivo Excel"}), 
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

            # Leer el archivo y procesarlo
            excel_data = pd.read_excel(BytesIO(file.read()))
            _logger.info(f"Archivo recibido: {file.filename}. Contenido: {excel_data.head()}")

            # Contadores para estadísticas
            created_count = 0
            skipped_count = 0

            # Mapeo de valores de género
            gender_mapping = {
                'M': 'male',
                'F': 'female'
            }

            # Verificar y crear registros de estudiantes
            for _, row in excel_data.iterrows():
                # Mapear género
                gender = gender_mapping.get(row['Genero'], 'male')  # Valor predeterminado: 'male'

                # Verificar si el estudiante ya existe
                if request.env['school.student'].sudo().search_count([('name', '=', row['Nombre']), ('email', '=', row['Email'])]) == 0:
                    request.env['school.student'].sudo().create({
                        'cuenta': row['Cuenta'],
                        'name': row['Nombre'],
                        'email': row['Email'],
                        'age': row.get('Edad', 0),
                        'gender': gender,
                    })
                    created_count += 1
                else:
                    _logger.info(f"Registro omitido (ya existe): {row['Nombre']} - {row['Email']}")
                    skipped_count += 1

            # Respuesta exitosa con estadísticas
            return Response(
                json.dumps({
                    "status": "success",
                    "message": "Archivo procesado exitosamente",
                    "created": created_count,
                    "skipped": skipped_count
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