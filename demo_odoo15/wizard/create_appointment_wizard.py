from odoo import models, fields, api, _


class CreateAppointment(models.TransientModel):
    _name = 'create.appointment'
    _description = 'Create Appointment Wizard'

    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    appointment_date = fields.Date(string="Appointment Date", required=False)

    def action_create_appointment(self):
        vals = {
            'patient_id': self.patient_id.id,
            'gender': self.patient_id.gender,
            'doctor_id': self.doctor_id.id,
            'appointment_date': self.appointment_date
        }
        appointment_rec = self.env['hospital.appointment'].create(vals)
        print(f"Appointment-----{appointment_rec}")
        return {
            'name': _('Appointment'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hospital.appointment',
            'res_id': appointment_rec.id,
            'target': 'new'
        }

    def action_view_appointment1(self):
        # Method : 01
        action = self.env.ref('demo_odoo15.action_hospital_appointment').read()[0]
        action['domain'] = [('patient_id', '=', self.patient_id.id)]
        return action

    def action_view_appointment2(self):
        # Method : 03
        action = self.env['ir.actions.actions']._for_xml_id('demo_odoo15.action_hospital_appointment')
        action['domain'] = [('patient_id', '=', self.patient_id.id)]
        return action

    def action_view_appointment3(self):
        # Method : 02
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointment',
            'rel_model': 'hospital.appointment',
            'view_type': 'form',
            'domain': [('patient_id', '=', self.patient_id.id)],
            'view_mode': 'form',
            'target': 'current',
        }
