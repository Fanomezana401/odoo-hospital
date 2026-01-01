from odoo import models, fields, api

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Dossier Patient'
    _order = 'name'
    _inherits = {'res.partner': 'partner_id'}
    _inherit = ['mail.thread', 'mail.activity.mixin']

    partner_id = fields.Many2one('res.partner', string='Contact lié', required=True, ondelete='cascade')
    date_of_birth = fields.Date(string='Date de naissance')
    cin = fields.Char(string='CIN / Identifiant', index=True)
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string='Rendez-vous')

    def name_get(self):
        res = []
        for rec in self:
            name = rec.name or "Nouveau Patient"
            display = f"{name} ({rec.cin})" if rec.cin else name
            res.append((rec.id, display))
        return res