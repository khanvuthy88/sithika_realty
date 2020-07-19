from odoo import models, fields, api


class ResGroup(models.Model):
    _inherit = ['res.groups']

    property_per_day = fields.Integer()
    project_per_day = fields.Integer()
    website_user_group = fields.Boolean(default=False)
