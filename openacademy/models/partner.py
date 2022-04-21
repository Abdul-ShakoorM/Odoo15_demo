from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "res.partner"

    instructor = fields.Boolean(string='instructor')
