from odoo import models, fields, api
from odoo.exceptions import ValidationError

class DoctorSlot(models.Model):
    _name = 'hospital.doctor.slot'
    _description = 'Indisponibilité Docteur'
    _order = 'start_dt'

    name = fields.Char(string='Titre', compute='_compute_name')
    doctor_id = fields.Many2one('res.users', string='Docteur', required=True)
    start_dt = fields.Datetime(string='Début', required=True)
    end_dt = fields.Datetime(string='Fin', required=True)
    
    slot_type = fields.Selection([
        ('busy', 'Occupé / Conférence'),
        ('available', 'Disponible (Informatif)'),
    ], string="Type", default='busy', required=True)

    def _compute_name(self):
        for r in self:
            label = "Indisponible" if r.slot_type == 'busy' else "Libre"
            r.name = f"{r.doctor_id.name} ({label})"

    @api.constrains('start_dt', 'end_dt')
    def _check_dates(self):
        for r in self:
            if r.start_dt >= r.end_dt:
                raise ValidationError("La date de début doit précéder la fin.")