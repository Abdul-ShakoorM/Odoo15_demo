from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _description = "Hospital Doctor"
    _rec_name = "doctor_name"
    _order = "reference desc"

    doctor_name = fields.Char(string='Name', required=True)
    reference = fields.Char(string='Doctor Reference', required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))
    age = fields.Integer(string='Age', tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')], required=True, default='male')
    note = fields.Text(string='Description')
    image = fields.Binary(string='Patient Image')
    appointment_count = fields.Integer(string='Appointments', compute='get_appointment_count')
    active = fields.Boolean(string='Active', default=True)

    def get_appointment_count(self):
        for rec in self:
            count = self.env['hospital.appointment'].search_count([('doctor_id', '=', rec.id)])
            rec.appointment_count = count

    @api.model
    def create(self, values):
        if not values.get('note'):
            values['note'] = 'New Doctor'
        if values.get('reference', _('New')) == _('New'):
            values['reference'] = self.env['ir.sequence'].next_by_code('hospital.doctor') or _('New')
        return super(HospitalDoctor, self).create(values)

    def copy(self, default=None):
        print("Successfully")
        if default is None:
            default = {}
        if not default.get('doctor_name'):
            default['doctor_name'] = _("%s (copy)", self.doctor_name)
        rec = super(HospitalDoctor, self).copy(default)
        return rec

    # Constraints
    @api.constrains('doctor_name')
    def _check_name(self):
        for rec in self:
            print("test")
            patients = self.env['hospital.doctor'].search([('doctor_name', '=', rec.doctor_name), ('id', '!=', rec.id)])
            if patients:
                raise ValidationError(f"Name {rec.doctor_name} already exist")

    @api.constrains('age')
    def _check_age(self):
        for rec in self:
            if rec.age == 0:
                raise ValidationError(f"age can't be zero")

    # @api.multi
    def open_doctor_appointments(self):
        return {
            'name': _('Appointments'),
            'domain': [('doctor_id', '=', self.id)],
            'context': {'default_doctor_id': self.id},
            'view_type': 'form',
            'res_model': 'hospital.appointment',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }
