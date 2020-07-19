from odoo import models, fields, api


class Advertising(models.Model):
    _name = 'khmerrealty.advertising'
    _inherit = ['mail.thread']

    name = fields.Char()
    ads_link = fields.Char()
    active = fields.Boolean(default=True)
    show_in = fields.Selection([
        ('blog_post', 'Blog Post'),
        ('property', 'Property'),
        ('single_property', 'Single Property')], default='blog_post')
    feature_image = fields.Image(max_width=1920, max_height=1920)
