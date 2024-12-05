from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Class(models.Model):
    _name = 'school.class'
    _description = 'Class Management'

    name = fields.Char(string='Class Name', required=True)
    code = fields.Char(string='Class Code', required=True)  # Puede repetirse
    section = fields.Char(string='Section', required=True)  # Nueva sección
    hour = fields.Float(string='Hour', required=True)  # Horario
    year = fields.Integer(string='Year', required=True, default=lambda self: fields.Date.today().year)
    period = fields.Selection(
        [('1', 'First Semester'), ('2', 'Second Semester'), ('3', 'Third Semester')],
        string='Period',
        required=True
    )
    active = fields.Boolean(string='Active', default=True)

    # Relación con docentes
    docent_id = fields.Many2one(
        'school.docent',
        string='Docent',
        required=True,
        ondelete='cascade'
    )

    # Relación con estudiantes
    student_ids = fields.Many2many(
        'school.student',
        'class_student_rel',
        'class_id',
        'student_id',
        string='Students'
    )

    _sql_constraints = [
        ('unique_class_combination', 
         'UNIQUE(code, section, hour, year, period)', 
         'Ya existe una clase con el mismo código, sección, horario, año y período.')
    ]

    @api.constrains('hour')
    def _check_hour(self):
        for record in self:
            if record.hour <= 0 or record.hour >= 24:
                raise ValidationError("La hora debe estar entre 1 y 23.")

    @api.constrains('student_ids')
    def _check_students(self):
        for record in self:
            # Verificar que los estudiantes estén activos
            for student in record.student_ids:
                if not student.active:
                    raise ValidationError(f"El estudiante {student.name} no está activo y no puede ser asignado a la clase.")
