from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"
    _order = "reference desc"

    patient_name = fields.Char(string='Name', required=True)
    age = fields.Integer('Age', tracking=True, required=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')], required=True, default='male')
    note = fields.Text(string='Description')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], string="Status", default='draft', tracking=True)

    reference = fields.Char(string='Patient Reference', required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))
    responsible_id = fields.Many2one('res.partner', string="Responsible")
    appointment_count = fields.Integer(string='Appointments', compute='get_appointment_count')
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id',
                                      string='Appointments')
    image = fields.Binary(string='Patient Image')

    def get_appointment_count(self):
        for rec in self:
            count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])
            rec.appointment_count = count

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
            values['note'] = 'New Patient'
        if values.get('reference', _('New')) == _('New'):
            values['reference'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('New')
        return super(HospitalPatient, self).create(values)

        # Constraints

    @api.constrains('patient_name')
    def _check_name(self):
        for rec in self:
            print("test")
            patients = self.env['hospital.patient'].search(
                [('patient_name', '=', rec.patient_name), ('id', '!=', rec.id)])
            if patients:
                raise ValidationError(f"Name {rec.patient_name} already exist")

    @api.constrains('age')
    def _check_age(self):
        for rec in self:
            if rec.age == 0:
                raise ValidationError(f"age can't be zero")

    def name_get(self):
        result = []
        for rec in self:
            patient_name = '[' + rec.reference + "] " + rec.patient_name
            result.append((rec.id, patient_name))
        return result


    def open_patient_appointments(self):
        return {
            'name': _('Appointments'),
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
            'view_type': 'form',
            'res_model': 'hospital.appointment',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }
