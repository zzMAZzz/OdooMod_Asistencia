
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Student(models.Model):
    _name = 'school.student'
    _description = 'Student Management'

    name = fields.Char(string='Name', required=True)
    cuenta = fields.Char(string='Account Number', required=True)
    email = fields.Char(string='Email', required=True)
    age = fields.Integer(string='Age')
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')],
        string='Gender',
    )
    active = fields.Boolean(string='Active', default=True)

    # Relación con clases
    class_ids = fields.Many2many(
        'school.class',
        'class_student_rel',
        'student_id',
        'class_id',
        string='Classes'
    )

    # Restricciones SQL para evitar duplicados
    _sql_constraints = [
        ('unique_cuenta', 'UNIQUE(cuenta)', 'El número de cuenta debe ser único.'),
        ('unique_email', 'UNIQUE(email)', 'El correo electrónico debe ser único.'),
    ]

    # Validación Python adicional (opcional)
    @api.constrains('email')
    def _check_email_format(self):
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        for student in self:
            if not re.match(email_regex, student.email):
                raise ValidationError('El correo debe tener un formato válido.')