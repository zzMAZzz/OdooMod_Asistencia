from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Docent(models.Model):
    _name = 'school.docent'
    _description = 'Docent Management'

    name = fields.Char(string='Name', required=True)
    cuenta = fields.Char(string='Account Number', required=True)
    email = fields.Char(string='Email', required=True)

    active = fields.Boolean(string='Active', default=True)

    # Relación con clases
    class_ids = fields.One2many(
        'school.class',
        'docent_id',
        string='Classes'
    )

    @api.constrains('cuenta')
    def _check_unique_cuenta(self):
        for record in self:
            # Check if there's another record with the same account number
            if self.search_count([('cuenta', '=', record.cuenta)]) > 1:
                raise ValidationError("The account number must be unique.")
