from odoo import models, fields, api


class SlideShow(models.Model):
    _name = 'khmerrealty.slide'
    _inherit = ['mail.thread']

    name = fields.Char(required=True)
    ads_link = fields.Char()
    active = fields.Boolean(default=True)
    show_in = fields.Selection([('top_slide', 'Top Slide'), ('home_below_top', 'Below Top Slide')], default='top_slide',
                               required=True)
    feature_image = fields.Image(max_width=1920, max_height=1920, required=True)
    image_540 = fields.Image("Image 540", related="feature_image", max_width=540, max_height=330)
