from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import timedelta

class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Rendez-vous et Dossier Médical'
    _order = 'appointment_dt desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Référence', compute='_compute_name', store=True)
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True, tracking=True)
    doctor_id = fields.Many2one('res.users', string='Docteur', required=True, default=lambda self: self.env.user, tracking=True)
    appointment_dt = fields.Datetime(string='Date & Heure', required=True, tracking=True, default=fields.Datetime.now)
    duration = fields.Float(string="Durée (h)", default=0.5)
    appointment_end_dt = fields.Datetime(string='Date Fin', compute='_compute_end_dt', store=True)

    state = fields.Selection([
        ('pending', 'En attente'),
        ('ongoing', 'Consultation'),
        ('done', 'Terminé'),
        ('cancel', 'Annulé'),
    ], default='pending', tracking=True)

    appointment_type = fields.Selection([
        ('first', 'Consultation (300 dhs)'),
        ('control', 'Contrôle (Gratuit)'),
    ], string="Type de visite", default='first', required=True)

    # --- Dossier Médical ---
    temperature = fields.Float(string='Température (°C)', groups="hospital_core.group_doctor")
    weight = fields.Float(string='Poids (kg)', groups="hospital_core.group_doctor")
    blood_pressure = fields.Char(string='Tension Artérielle', groups="hospital_core.group_doctor")
    heart_rate = fields.Integer(string='Fréquence Cardiaque', groups="hospital_core.group_doctor")
    diagnostic = fields.Text(string='Diagnostic / Bilan', groups="hospital_core.group_doctor")
    prescription = fields.Text(string='Ordonnance', groups="hospital_core.group_doctor")
    act_code = fields.Char(string='Code acte', groups="hospital_core.group_doctor")

    invoice_id = fields.Many2one('account.move', string='Facture', readonly=True, copy=False)
    payment_state = fields.Selection(related='invoice_id.payment_state', string="État Paiement")

    # --- Logique Automatique Facturation ---
    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        if self.patient_id:
            count = self.search_count([
                ('patient_id', '=', self.patient_id.id), 
                ('state', '!=', 'cancel')
            ])
            # Si count == 1, cela signifie qu'il a déjà fait sa 1ère visite, donc celle-ci est la 2ème (control)
            self.appointment_type = 'control' if count == 1 else 'first'

    @api.depends('patient_id', 'appointment_dt')
    def _compute_name(self):
        for r in self:
            date_str = r.appointment_dt.strftime('%d/%m/%Y %H:%M') if r.appointment_dt else ''
            r.name = f"{r.patient_id.name or 'Nouveau'} - {date_str}"

    @api.depends('appointment_dt', 'duration')
    def _compute_end_dt(self):
        for r in self:
            if r.appointment_dt:
                r.appointment_end_dt = r.appointment_dt + timedelta(hours=r.duration)
            else:
                r.appointment_end_dt = False

    # --- CONTRAINTE DE DISPONIBILITÉ ---
    @api.constrains('appointment_dt', 'duration', 'doctor_id')
    def _check_doctor_availability(self):
        for r in self:
            if not r.appointment_dt or not r.appointment_end_dt:
                continue

            # 1. Vérifier les indisponibilités dans le planning (Doctor Slots)
            busy_slots = self.env['hospital.doctor.slot'].search([
                ('doctor_id', '=', r.doctor_id.id),
                ('slot_type', '=', 'busy'),
                ('start_dt', '<', r.appointment_end_dt),
                ('end_dt', '>', r.appointment_dt),
            ])
            if busy_slots:
                raise ValidationError(_("Le docteur %s est marqué comme indisponible (Planning) sur ce créneau.") % r.doctor_id.name)

            # 2. Vérifier s'il n'y a pas déjà un autre RDV en cours sur ce créneau
            overlapping_appointment = self.search([
                ('id', '!=', r.id), # Ne pas se comparer soi-même
                ('doctor_id', '=', r.doctor_id.id),
                ('state', 'not in', ['cancel']),
                ('appointment_dt', '<', r.appointment_end_dt),
                ('appointment_end_dt', '>', r.appointment_dt),
            ])
            if overlapping_appointment:
                raise ValidationError(_("Le docteur %s a déjà un autre rendez-vous prévu à cette heure.") % r.doctor_id.name)

    # --- Actions d'état (Réservées Médecin) ---
    def action_start(self):
        if not self.env.user.has_group('hospital_core.group_doctor'):
            raise UserError("Seul le médecin peut démarrer la consultation.")
        self.write({'state': 'ongoing'})

    def action_finish(self):
        if not self.env.user.has_group('hospital_core.group_doctor'):
            raise UserError("Seul le médecin peut terminer la consultation.")
        self.write({'state': 'done'})

    # --- Facturation (Réservée Admin/Secrétaire) ---
    def action_create_invoice(self):
        for r in self:
            if r.invoice_id:
                raise UserError("Facture déjà générée.")
            price = 300.0 if r.appointment_type == 'first' else 0.0
            invoice_vals = {
                'move_type': 'out_invoice',
                'partner_id': r.patient_id.partner_id.id,
                'invoice_date': fields.Date.context_today(self),
                'invoice_line_ids': [(0, 0, {
                    'name': f"Consultation médicale: {r.name}",
                    'quantity': 1,
                    'price_unit': price,
                })],
            }
            r.invoice_id = self.env['account.move'].create(invoice_vals)