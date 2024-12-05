from odoo import models, fields

class Attendance(models.Model):
    _name = 'school.attendance'
    _description = 'Attendance Management'

    date = fields.Date(
        string='Date', 
        required=True, 
        default=fields.Date.today
    )
    class_id = fields.Many2one(
        'school.class', 
        string='Class', 
        required=True
    )
    student_id = fields.Many2one(
        'school.student', 
        string='Student', 
        required=True
    )
    status = fields.Selection(
        [
            ('present', 'Present'),
            ('absent', 'Absent'),
            ('excused', 'Excused')  # Nuevo estado añadido
        ],
        string='Status',
        required=True,
        default='present'
    )