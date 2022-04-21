from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _description = "Hospital Appointment"
    _rec_name = 'reference'

    reference = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))
    patient_id = fields.Many2one('hospital.patient', string="Patient")
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor", required=True)
    age = fields.Integer(string='Age', related='patient_id.age')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')], required=True)
    note = fields.Text(string='Description')
    # Status bar states
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], string="Status", default='draft', tracking=True)

    appointment_date = fields.Date(string='Appointment Date')
    checkup_date = fields.Datetime(string='Check Up Time')
    prescription = fields.Text(string="Prescription")
    prescription_line_ids = fields.One2many('appointment.prescription.lines', 'appointment_id',
                                            string='Prescription Lines')

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    @api.model
    def create(self, values):
        if not values.get('note'):
            values['note'] = 'New Appointment'
        if values.get('reference', _('New')) == _('New'):
            values['reference'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')
        return super(HospitalAppointment, self).create(values)

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        if self.patient_id:
            if self.patient_id.gender:
                self.gender = self.patient_id.gender
            if self.patient_id.note:
                self.note = self.patient_id.note
        else:
            self.gender = ''
            self.note = 'New Patient'

    def unlink(self):
        if self.state == 'done':
            raise ValidationError(f"You can't delete {self.reference} as it is in done state")
        rec = super(HospitalAppointment, self).unlink()
        return rec


class AppointmentPrescriptionLines(models.Model):
    _name = "appointment.prescription.lines"
    _description = "Appointment Prescription Lines"

    name = fields.Char(string='Medicine', required=True)
    qty = fields.Integer(string='Quantity')
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
