# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class OpenAcademyCourse(models.Model):
    _name = 'openacademy.course'
    _description = 'Open Acadmey Course'

    name = fields.Char('Name')
    description = fields.Text('Description')
    title = fields.Char('Title', readonly=True,
                        default=lambda self: _('New'))
    responsible_user = fields.Many2one('res.users', 'Responsible User')
    session_id = fields.One2many('openacademy.session','course_id', 'Session')

    @api.model
    def create(self, values):
        if values.get('title', _('New')) == _('New'):
            values['title'] = self.env['ir.sequence'].next_by_code('openacademy.course') or _('New')
        return super(OpenAcademyCourse, self).create(values)
