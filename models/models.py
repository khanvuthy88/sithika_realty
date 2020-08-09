# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import UserError
from odoo.addons.http_routing.models.ir_http import slug
from odoo.tools.translate import html_translate
from odoo.tools import html2plaintext


class Website(models.Model):
    _inherit = 'website'

    footer_description = fields.Html()
    footer_logo = fields.Image(max_width=350, max_height=90)
    website_call_center = fields.Char()


class WebsiteConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    facebook_icon = fields.Image(max_width=30, max_height=30)
    facebook_url = fields.Char()

    instagram_icon = fields.Image(max_width=30, max_height=30)
    instagram_url = fields.Char()

    linkedin_icon = fields.Image(max_width=30, max_height=30)
    linkedin_url = fields.Char()

    twitter_icon = fields.Image(max_width=30, max_height=30)
    twitter_url = fields.Char()

    youtube_icon = fields.Image(max_width=30, max_height=30)
    youtube_url = fields.Char()

    tiktok_icon = fields.Image(max_width=30, max_height=30)
    tiktok_url = fields.Char()


class PropertyLocation(models.Model):
    _name = 'khmerrealty.property.location'
    _inherit = ['mail.thread', "website.seo.metadata", 'website.published.multi.mixin']

    name = fields.Char(translate=html_translate)
    parent_id = fields.Many2one('khmerrealty.property.location')
    feature_image = fields.Image(max_width=1920, max_height=1920)
    feature_location = fields.Boolean()
    sequence = fields.Integer()

    def _compute_website_url(self):
        super(PropertyLocation, self)._compute_website_url()
        for record in self:
            record.website_url = "property/location/%s" % slug(record)

    def property_by_location_buy_rent(self, location, category):
        property_obj = self.env['khmerrealty.property'].search_count([
            ('property_category', '=', category),
            ('property_city', '=', location)])
        return property_obj


class PropertyAmenity(models.Model):
    _name = 'khmerrealty.property.amenity'

    name = fields.Char(required=True, translate=html_translate)
    icons_font = fields.Char('Icon')


class PropertySecurity(models.Model):
    _name = 'khmerrealty.property.security'

    name = fields.Char(required=True, translate=html_translate)
    icons_font = fields.Char('Icon')


class PropertyFeature(models.Model):
    _name = 'khmerrealty.property.feature'

    name = fields.Char(required=True, translate=html_translate)
    icons_font = fields.Char('Icon')


class PropertyType(models.Model):
    _name = 'khmerrealty.type'
    name = fields.Char(required=True, translate=html_translate)


class ProjectHighlights(models.Model):
    _name = 'khmerrealty.project.highlights'

    name = fields.Char(translate=html_translate, required=True)


class Property(models.Model):
    _name = 'khmerrealty.property'
    _inherit = ['mail.thread', "website.seo.metadata", 'website.published.multi.mixin']
    _mail_post_access = 'read'


    @api.model
    def _get_default_property_author(self):
        user = self.env['res.users'].search([('id', '=', self.env.uid)])
        if user:
            partner = self.env['res.partner'].search([('id', '=', user.partner_id.id)])
            if partner:
                return partner.id
            else:
                return

    active = fields.Boolean(default=True)
    property_type = fields.Many2one('khmerrealty.type', required=True)
    property_author = fields.Many2one('res.partner', default=_get_default_property_author, required=True)
    name = fields.Char(translate=html_translate, required=True)
    description = fields.Text(translate=html_translate, sanitize=False, required=True)
    property_status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('has_sole', 'Sole'),
        ('has_rent', 'Rent')], default='active', string='Status')
    property_category = fields.Selection([
        ('buy', 'Buy'),
        ('rent', 'Rent')], default='buy')
    feature = fields.Many2many('khmerrealty.property.feature')
    amenity = fields.Many2many('khmerrealty.property.amenity')
    security = fields.Many2many('khmerrealty.property.security')
    property_city = fields.Many2one('khmerrealty.property.location', string='Province',
                                    domain=[('parent_id', '=', False)])
    property_district = fields.Many2one('khmerrealty.property.location', string='District')
    property_commune = fields.Many2one('khmerrealty.property.location', string='Commune')
    street_name = fields.Char(translate=html_translate)
    street_number = fields.Char(translate=html_translate)
    floor_level = fields.Char()
    price = fields.Float(digits=(12, 2), required=True)
    price_per_m = fields.Float(digits=(12, 2), required=True)
    display_price = fields.Boolean(default=True)
    number_bedroom = fields.Integer(required=True)
    number_bathroom = fields.Integer(required=True)
    property_size = fields.Float()
    property_facing = fields.Char()
    car_space = fields.Integer(required=True)
    floor_area_per_m = fields.Float(digits=(12, 2), required=True)
    land_area_per_m = fields.Float(digits=(12, 2), required=True)
    total_floor = fields.Integer()
    feature_image = fields.Image(max_width=1080, max_height=1080, required=True)
    image_255 = fields.Image("Image 128", related="feature_image", max_width=255, max_height=210, store=True)
    image_gallery = fields.Many2many('ir.attachment', string="Images", required=True)
    property_create_date = fields.Date(default=datetime.today())
    short_description = fields.Text(compute="_compute_short_description")
    property_address = fields.Char(compute="_compute_property_address")
    readable_id = fields.Char(compute="_compute_property_id")
    feature_image_src = fields.Char(compute="_compute_feature_image_src")

    def _compute_feature_image_src(self):
        for record in self:
            image_url = '/web/image/%s' + record.feature_image.id
            record.feature_image_src = image_url

    def _compute_property_id(self):
        for record in self:
            record.readable_id = 'SRPID{}'.format(record.id)

    @api.depends('property_city.name', 'property_district.name', 'property_commune.name')
    def _compute_property_address(self):
        for record in self:
            record.property_address = '{} > {} > {}'.format(record.property_city.name, record.property_district.name,
                                                            record.property_commune.name)

    def _compute_short_description(self):
        for record in self:
            content = html2plaintext(record.description).replace('\n', ' ')
            record.short_description = content[:200] + '...'

    @api.model
    def create(self, val):
        allow_create = False
        user_group = self.env.user.groups_id
        property_today = self.env['khmerrealty.property'].search_count([
            ('property_create_date', '=', datetime.today()),
            ('create_uid', '=', self.env.user.id)
        ])
        for group in user_group:
            if group.website_user_group and group.property_per_day > property_today:
                print(group.property_per_day)
                allow_create = True
                break
        if allow_create:
            return super(Property, self).create(val)
        else:
            raise UserError("You are not allow to post more than {} per day".format(property_today))

    def _compute_image_128(self):
        for record in self:
            record.image_128 = record.feature_image

    @api.onchange('property_city')
    def onchange_property_city(self):
        self.property_district = []
        self.property_commune = []
        return {
            'domain': {
                'property_district': [
                    ('parent_id', '=', self.property_city.id)
                ]
            }
        }

    @api.onchange('property_district')
    def onchange_property_district(self):
        self.property_commune = []
        return {
            'domain': {
                'property_commune': [
                    ('parent_id', '=', self.property_district.id)
                ]
            }
        }

    def _compute_website_url(self):
        super(Property, self)._compute_website_url()
        for record in self:
            print(record.website_id)
            record.website_url = "/property/%s/%s" % (slug(record.property_type), slug(record))

    def _default_website_meta(self):
        res = super(Property, self)._default_website_meta()
        res['default_opengraph']['og:description'] = res['default_twitter']['twitter:description'] = self.short_description
        res['default_opengraph']['og:type'] = 'article'
        res['default_opengraph']['article:published_time'] = self.create_date
        res['default_opengraph']['fb:app_id'] = '290178345404898'
        res['default_opengraph']['article:modified_time'] = self.write_date
        res['default_opengraph']['article:tag'] = self.feature.mapped('name')
        res['default_opengraph']['og:title'] = res['default_twitter']['twitter:title'] = self.name
        res['default_opengraph']['og:image'] = res['default_twitter']['twitter:image'] = self.env['website'].image_url(self, 'feature_image')
        res['default_meta_description'] = self.short_description
        return res

    def active_property_domain(self):
        return [('active', '=', True)]


class Project(models.Model):
    _name = 'khmerrealty.project'
    _inherit = ['mail.thread', "website.seo.metadata", 'website.published.multi.mixin']

    @api.model
    def _get_default_property_author(self):
        user = self.env['res.users'].search([('id', '=', self.env.uid)])
        if user:
            partner = self.env['res.partner'].search([('id', '=', user.partner_id.id)])
            if partner:
                return partner.id
            else:
                return

    active = fields.Boolean(default=True)
    project_author = fields.Many2one('res.partner', default=_get_default_property_author, required=True)
    name = fields.Char(translate=True, required=True)
    description = fields.Text(translate=True, required=True)
    project_status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('has_sole', 'Sole'),
        ('has_rent', 'Rent')], default='active', string='Status')
    feature = fields.Many2many('khmerrealty.property.feature', required=True)
    project_highlight = fields.Many2many('khmerrealty.project.highlights', required=True)
    amenity = fields.Many2many('khmerrealty.property.amenity', required=True)
    security = fields.Many2many('khmerrealty.property.security', required=True)
    project_city = fields.Many2one('khmerrealty.property.location', string='Province',
                                   domain=[('parent_id', '=', False)])
    project_district = fields.Many2one('khmerrealty.property.location', string='District')
    project_commune = fields.Many2one('khmerrealty.property.location', string='Commune')
    street_name = fields.Char(translate=True, required=True)
    street_number = fields.Char(translate=True, required=True)
    total_unite = fields.Float(digits=(12, 2), required=True)
    unite_type = fields.Many2one('khmerrealty.type', required=True)
    price = fields.Float(digits=(12, 2), required=True)
    bedroom_in_unite = fields.Integer()
    floor_area = fields.Float(digits=(12, 2), required=True)
    floor = fields.Float(digits=(12, 2), required=True)
    complete_year = fields.Integer()
    feature_image = fields.Image(max_width=1920, max_height=1920, required=True)
    image_128 = fields.Image("Image 128", compute='_compute_image_128')
    image_255 = fields.Image("Image 255", related="feature_image", max_width=255, max_height=210, store=True)
    image_gallery = fields.Many2many('ir.attachment', string="Images", required=True)
    display_price = fields.Boolean(default=True)
    short_description = fields.Text(compute="_compute_short_description")
    readable_id = fields.Char(compute="_compute_readable_id")
    feature_image_src = fields.Char(compute="_compute_feature_image_src")


    def _compute_feature_image_src(self):
        for record in self:
            image_url = '/web/image/%s' + record.feature_image.id
            record.feature_image_src = image_url

    def _compute_readable_id(self):
        for record in self:
            record.readable_id = 'SRPID{}'.format(record.id)

    def _compute_website_url(self):
        super(Project, self)._compute_website_url()
        for record in self:
            record.website_url = "/project/%s/%s" % (slug(record.unite_type), slug(record))

    def _compute_short_description(self):
        for record in self:
            content = html2plaintext(record.description).replace('\n', ' ')
            record.short_description = content[:200] + '...'

    def _compute_image_128(self):
        for record in self:
            record.image_128 = record.feature_image

    def _default_website_meta(self):
        res = super(Project, self)._default_website_meta()
        res['default_opengraph']['og:description'] = res['default_twitter']['twitter:description'] = self.short_description
        res['default_opengraph']['og:type'] = 'article'
        res['default_opengraph']['article:published_time'] = self.create_date
        res['default_opengraph']['article:modified_time'] = self.write_date
        res['default_opengraph']['article:tag'] = self.feature.mapped('name')
        res['default_opengraph']['fb:app_id'] = '290178345404898'
        res['default_opengraph']['og:title'] = res['default_twitter']['twitter:title'] = self.name
        res['default_opengraph']['og:image'] = res['default_twitter']['twitter:image'] = self.env['website'].image_url(self, 'feature_image')
        res['default_meta_description'] = self.short_description
        return res

    @api.onchange('property_city')
    def onchange_project_city(self):
        self.project_district = []
        self.project_commune = []
        return {
            'domain': {
                'project_district': [
                    ('parent_id', '=', self.project_city.id)
                ]
            }
        }

    @api.onchange('project_district')
    def onchange_project_district(self):
        self.project_commune = []
        return {
            'domain': {
                'project_commune': [
                    ('parent_id', '=', self.project_district.id)
                ]
            }
        }

    def get_attachment_src(self, attachment_id):
        attachment = self.env['ir.attachment'].sudo().search([('id', '=', attachment_id)])
        return attachment.image_src


class BlogPost(models.Model):
    _inherit = 'blog.post'

    feature_image = fields.Image(max_width=1920, max_height=1920, required=True)
    image_384 = fields.Image("Image 384", related="feature_image", max_width=384, max_height=217, store=True)
    image_825 = fields.Image("Image 825", related="feature_image", max_width=825, max_height=465, store=True)
    short_description = fields.Char(compute='_compute_short_description')

    def _compute_short_description(self):
        for record in self:
            content = html2plaintext(record.subtitle).replace('\n', ' ')
            record.short_description = content[:70] + '...'

    def _default_website_meta(self):
        res = super(BlogPost, self)._default_website_meta()
        res['default_opengraph']['og:description'] = res['default_twitter']['twitter:description'] = self.subtitle
        res['default_opengraph']['og:type'] = 'article'
        res['default_opengraph']['article:published_time'] = self.post_date
        res['default_opengraph']['article:modified_time'] = self.write_date
        res['default_opengraph']['fb:app_id'] = '290178345404898'
        res['default_opengraph']['article:tag'] = self.tag_ids.mapped('name')
        res['default_opengraph']['og:image'] = res['default_twitter']['twitter:image'] = self.env['website'].image_url(self, 'feature_image')
        res['default_opengraph']['og:title'] = res['default_twitter']['twitter:title'] = self.name
        res['default_meta_description'] = self.subtitle
        return res


class ResPartner(models.Model):
    _inherit = 'res.partner'

    description_website = fields.Html(translate=True)
    feature_agency = fields.Boolean(default=False)
    feature_agent = fields.Boolean(default=False)
    city_vt = fields.Many2one('khmerrealty.property.location', string='Province',
                              domain=[('parent_id', '=', False)])
    district_vt = fields.Many2one('khmerrealty.property.location', string='District')
    commune_vt = fields.Many2one('khmerrealty.property.location', string='Commune')
    agent_website_url = fields.Char(compute="_compute_agent_website_url")
    phone_number_website = fields.Char(compute='_compute_phone_number_with')
    website_short_description = fields.Text('Website Partner Short Description', translate=True, compute='_compute_short_description')

    def _compute_short_description(self):
        for record in self:
            content = html2plaintext(record.description_website).replace('\n', ' ')
            record.website_short_description = content[:200] + '...'


    def _default_website_meta(self):
        res = super(ResPartner, self)._default_website_meta()
        res['default_opengraph']['og:description'] = res['default_twitter']['twitter:description'] = self.website_short_description
        res['default_opengraph']['og:type'] = 'article'
        res['default_opengraph']['article:published_time'] = self.create_date
        res['default_opengraph']['article:modified_time'] = self.write_date
        res['default_opengraph']['fb:app_id'] = '290178345404898'
        res['default_opengraph']['og:title'] = res['default_twitter']['twitter:title'] = self.name
        res['default_opengraph']['og:image'] = res['default_twitter']['twitter:image'] = self.env['website'].image_url(self, 'image_1920')
        res['default_meta_description'] = self.website_short_description
        return res

    def _compute_phone_number_with(self):
        for record in self:
            tel_n = 'tel:+85589602525'
            if record.phone:
                tel_n = 'tel:' + record.phone if record.phone.startswith('+855') else 'tel:+855' + record.phone
            record.phone_number_website = tel_n

    def _compute_agent_website_url(self):
        for partner in self:
            partner.agent_website_url = "/agent/%s" % slug(partner)

    def _compute_website_url(self):
        super(ResPartner, self)._compute_website_url()
        for partner in self:
            partner.website_url = "/agency/%s" % slug(partner)

    @api.onchange('city_vt')
    def onchange_city_vt(self):
        self.district_vt = []
        self.commune_vt = []
        return {
            'domain': {
                'district_vt': [
                    ('parent_id', '=', self.city_vt.id)
                ]
            }
        }

    @api.onchange('district_vt')
    def onchange_district_vt(self):
        self.commune_vt = []
        return {
            'domain': {
                'commune_vt': [
                    ('parent_id', '=', self.district_vt.id)
                ]
            }
        }

    def get_project_by_agency(self, agency_id):
        property_count = self.env['khmerrealty.project'].search_count(
            [('project_author.parent_id', '=', agency_id.id)])
        return property_count

    def get_agent_by_agency_id(self, agency_id):
        agent_count = self.env['res.partner'].search_count([('parent_id', '=', agency_id.id)])
        if agent_count:
            return agent_count
        else:
            return 0

    def count_property_by_agency_id(self, agency_id):
        property_count = self.env['khmerrealty.property'].search_count(
            [('property_author.parent_id', '=', agency_id.id)])
        return property_count

    def count_property_by_agent(self, agent_id):
        property_count = self.env['khmerrealty.property'].search_count(
            [('property_author', '=', agent_id.id)])
        return property_count

    def count_property_by_agent_sold(self, agent_id):
        property_count = self.env['khmerrealty.property'].search_count(
            [('property_author', '=', agent_id.id), ('property_status', '=', 'has_sole')])
        return property_count


class IrAttachment(models.Model):
    _inherit = ['ir.attachment']

    public = fields.Boolean(default=True)
