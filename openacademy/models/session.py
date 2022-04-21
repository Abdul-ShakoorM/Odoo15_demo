# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class OpenAcademyCourse(models.Model):
    _name = 'openacademy.session'
    _description = 'Open Acadmey Session'
    _rec_name = 'instructor'

    start_date = fields.Date('Start Date')
    duration = fields.Char('Duration')
    no_of_seats = fields.Integer('No of Seats')
    instructor = fields.Many2one('res.partner', 'Instructor')
    course_id = fields.Many2one('openacademy.course', 'Course')


