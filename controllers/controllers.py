# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.controllers.main import QueryURL
from odoo.osv import expression
from odoo.addons.website.controllers.main import Website
from odoo.addons.website_blog.controllers.main import WebsiteBlog


class Website(Website):
    @http.route(auth='public')
    def index(self, data={}, **kw):
        super(Website, self).index(**kw)
        base_url = 'http://sithikarealty.com'
        show_slide = true
        has_property = False
        property_obj = request.env['khmerrealty.property']
        location_obj = request.env['khmerrealty.property.location'].search([('parent_id', '=', False)])
        slide_obj = request.env['khmerrealty.slide']
        blog_news_obj = request.env['blog.post']
        top_three_news = blog_news_obj.search([('blog_id', '=', 2)], limit=3, order='id desc')
        top_three_guide = blog_news_obj.search([('blog_id', '=', 1)], limit=3, order='id desc')
        popular_property_rent = property_obj.search([('property_category', '=', 'rent')],
                                                    limit=4, order='id desc')
        popular_property_buy = property_obj.search([('property_category', '=', 'buy')], limit=4,
                                                   order='id desc')
        feature_agency_home = request.env['res.partner'].search([('feature_agency', '=', True)], limit=4)
        slides = slide_obj.search([
            ('active', '=', True),
            ('show_in', '=', 'top_slide')], order='id desc')
        next_slides = slide_obj.search([
            ('active', '=', True),
            ('show_in', '=', 'home_below_top')], order='id desc')
        if popular_property_buy or popular_property_rent:
            has_property = True
        return http.request.render('khmerrealty.home_page', {
            'has_property': has_property,
            'location_obj': location_obj,
            'popular_property_buy': popular_property_buy,
            'popular_property_rent': popular_property_rent,
            'feature_agency_home': feature_agency_home,
            'top_locations': http.request.env['khmerrealty.property.location'].search([('feature_location', '=', True)],
                                                                                      limit=5, order='sequence'),
            'feature_project_home': http.request.env['khmerrealty.project'].search([], limit=4, order='id desc'),
            'top_three_news': top_three_news,
            'top_three_guide': top_three_guide,
            'slide_show': slides,
            'next_slides': next_slides,
            'base_url': base_url,
            'show_slide': show_slide,
        })


class WebsiteBlog(WebsiteBlog):
    @http.route(auth='public')
    def blog_post(self, data={}, **kw):
        super(WebsiteBlog, self).blog_post(**kw)
        article = request.env['blog.post'].search([('id', '=', kw.get('blog_post').id)], limit=1)
        advertising_images = request.env["khmerrealty.advertising"].search([('show_in', '=', 'blog_post')],
                                                                           limit=3)
        return http.request.render('khmerrealty.blog_post_single_article', {
            'article': article,
            'advertising_images': advertising_images,
        })


class Khmerrealty(http.Controller):
    _property_per_page = 4
    _agency_per_page = 12
    _property_search_page = 4
    _pager_step_ppg = 10

    @http.route('/property/search/rent/<string:search>', auth='public', website=True)
    def property_search(self, search, **kw):
        properties = http.request.env['khmerrealty.property'].search([
            ('property_type', '=', 'rent'),
            ('name', 'ilike', search), '|',
            ('description', 'ilike', search)
        ])
        return properties

    @http.route('/services/', auth='public', website=True)
    def index(self, **kw):
        has_property = False
        property_obj = request.env['khmerrealty.property']
        location_obj = request.env['khmerrealty.property.location'].search([('parent_id', '=', False)])
        slide_obj = request.env['khmerrealty.slide']
        blog_news_obj = request.env['blog.post']
        top_three_news = blog_news_obj.search([('blog_id', '=', 2)], limit=3, order='id desc')
        top_three_guide = blog_news_obj.search([('blog_id', '=', 1)], limit=3, order='id desc')
        popular_property_rent = property_obj.search([('property_category', '=', 'rent')],
                                                    limit=4, order='id desc')
        popular_property_buy = property_obj.search([('property_category', '=', 'buy')], limit=4,
                                                   order='id desc')
        feature_agency_home = request.env['res.partner'].search([('feature_agency', '=', True)], limit=4)
        slides = slide_obj.search([
            ('active', '=', True),
            ('show_in', '=', 'top_slide')], order='id desc')
        next_slides = slide_obj.search([
            ('active', '=', True),
            ('show_in', '=', 'home_below_top')], order='id desc')
        if popular_property_buy or popular_property_rent:
            has_property = True
        return http.request.render('khmerrealty.home_page', {
            'has_property': has_property,
            'location_obj': location_obj,
            'popular_property_buy': popular_property_buy,
            'popular_property_rent': popular_property_rent,
            'feature_agency_home': feature_agency_home,
            'top_locations': http.request.env['khmerrealty.property.location'].search([('feature_location', '=', True)],
                                                                                      limit=5, order='sequence'),
            'feature_project_home': http.request.env['khmerrealty.project'].search([], limit=4, order='id desc'),
            'top_three_news': top_three_news,
            'top_three_guide': top_three_guide,
            'slide_show': slides,
            'next_slides': next_slides,
        })

    @http.route(['/blog/news', '/blog/news/page/<int:page>'], auth='public', website=True)
    def blog_news(self, page=1, **kw):
        news_obj = request.env['blog.post']
        news_count = news_obj.search_count([('blog_id', '=', 2)])
        url = "/blog/news"
        pager = request.website.pager(url=url, total=news_count, page=page,
                                      step=6, scope=self._pager_step_ppg)
        news = news_obj.search([('blog_id', '=', 2)], limit=6, offset=pager['offset'])

        return http.request.render('khmerrealty.blog_post_list_template', {
            'banners': http.request.env['khmerrealty.advertising'].search([('show_in', '=', 'blog_post')], limit=3),
            'blog_obj': news,
            'blog_type': 'News',
            'pager': pager,
        })

    @http.route(['/blog/events', '/blog/events/page/<int:page>'], auth='public', website=True)
    def blog_events(self, page=1, **kw):
        news_obj = request.env['blog.post']
        news_count = news_obj.search_count([('blog_id', '=', 1)])
        url = "/blog/events"
        pager = request.website.pager(url=url, total=news_count, page=page,
                                      step=6, scope=self._pager_step_ppg)
        news = news_obj.search([('blog_id', '=', 1)], limit=6, offset=pager['offset'])

        return http.request.render('khmerrealty.render_blog_template', {
            'banners': http.request.env['khmerrealty.advertising'].search([('show_in', '=', 'blog_post')], limit=3),
            'blogs': news,
            'blog_type': 'Events',
            'pager': pager,
        })

    @http.route('/news/<model("blog.post"):obj>/', auth='public', website=True)
    def single_news(self, obj, **kw):
        return http.request.render('khmerrealty.single_news', {
            'post': obj,
            'advertising_images': http.request.env['khmerrealty.advertising'].search([('show_in', '=', 'blog_post')],
                                                                                     limit=3),
        })

    @http.route(['/property-listing/',
                 '/property-listing/page/<int:page>'], auth='public', website=True)
    def properties(self, page=1, **kw):
        property = request.env['khmerrealty.property']
        property_count = property.search_count([])
        url = "/property-listing"
        locations = request.env['khmerrealty.property.location'].search([('parent_id', '=', False)])
        property_type_obj = request.env['khmerrealty.type'].search([])
        pager = request.website.pager(url=url, total=property_count, page=page,
                                      step=self._property_per_page, scope=self._pager_step_ppg)
        return http.request.render('khmerrealty.property_listing', {
            'banners': http.request.env['khmerrealty.advertising'].search([('show_in', '=', 'property')], limit=3),
            'properties': property.search([], limit=self._property_per_page, offset=pager['offset']),
            'pager': pager,
            'property_location': locations,
            'property_type_obj': property_type_obj,
        })

    @http.route('/property/<model("khmerrealty.type"):property_type>/<model("khmerrealty.property"):record>',
                auth='public', website=True)
    def single_property(self, record, **kw):
        property_root_url = QueryURL('/property-listing')
        property_type_url = ''
        locations = request.env['khmerrealty.property.location'].search([('parent_id', '=', False)])
        if record.property_category == 'buy':
            property_type_url = '/property/buy'
        elif record.property_category == 'rent':
            property_type_url = '/property/rent'
        return http.request.render('khmerrealty.single_property', {
            'property': record,
            'banners': http.request.env['khmerrealty.advertising'].search([('show_in', '=', 'single_property')],
                                                                          limit=3),
            'related_property': http.request.env['khmerrealty.property'].search([
                ('id', '!=', record.id),
                ('property_type', 'in', [record.property_type.id])],
                limit=4, order='id desc'),
            'property_root_url': property_root_url,
            'property_type_url': property_type_url,
            'locations': locations,
        })

    @http.route(['/property/author/<model("res.partner"):author_id>/',
                 '/property/author/<model("res.partner"):author_id>/page/<int:page>'], auth='public', website=True)
    def property_by_author(self, author_id, page=1, **kw):
        properties = request.env['khmerrealty.property']
        property_count = properties.search_count([('property_author', '=', author_id.id)])
        if author_id:
            url = "/property/author/%s" % slug(author_id)
        pager = request.website.pager(url=url, total=property_count, page=page,
                                      step=self._property_per_page, scope=self._pager_step_ppg)
        return http.request.render('khmerrealty.property_by_author', {
            'banners': http.request.env['khmerrealty.advertising'].search([('show_in', '=', 'property')], limit=3),
            'properties': properties.search([('property_author', '=', author_id.id)], limit=self._property_per_page,
                                            offset=pager['offset']),
            'author': author_id,
            'pager': pager,
        })

    @http.route(['/property/location/<model("khmerrealty.property.location"):location_id>/',
                 '/property/location/<model("khmerrealty.property.location"):location_id>/page/<int:page>'],
                auth='public', website=True)
    def property_by_location(self, location_id, page=1, **kw):
        properties = request.env['khmerrealty.property']
        property_count = properties.search_count([('property_city', '=', location_id.id)])
        if location_id:
            url = "/property/location/%s" % slug(location_id)
        pager = request.website.pager(url=url, total=property_count, page=page,
                                      step=self._property_per_page, scope=self._pager_step_ppg)
        properties_obj = properties.search([('property_city', '=', location_id.id)], limit=self._property_per_page,
                                           offset=pager['offset'])
        return http.request.render('khmerrealty.property_listing', {
            'banners': http.request.env['khmerrealty.advertising'].search([('show_in', '=', 'property')], limit=3),
            'properties': properties_obj,
            'location': location_id,
            'property_location': http.request.env['khmerrealty.property.location'].search([('parent_id', '=', False)]),
            'pager': pager,
            'property_count': property_count,
        })

    @http.route(['/project-listing/',
                 '/project-listing/page/<int:page>'], auth='public', website=True)
    def projects(self, page=1, **kw):
        projects = request.env['khmerrealty.project']
        locations = request.env['khmerrealty.property.location'].search([('parent_id', '=', False)])
        property_type_obj = request.env['khmerrealty.type'].search([])
        project_count = projects.search_count([])
        url = "/project-listing"
        property_type = 'all'
        pager = request.website.pager(url=url, total=project_count, page=page,
                                      step=self._property_per_page, scope=self._pager_step_ppg)
        return http.request.render('khmerrealty.project_listing_page', {
            'banners': http.request.env['khmerrealty.advertising'].search([('show_in', '=', 'property')], limit=3),
            'projects': projects.search([], limit=self._property_per_page, offset=pager['offset']),
            'project_count': project_count,
            'pager': pager,
            'property_type': property_type,
            'locations': locations,
            'property_type_obj': property_type_obj,
        })

    @http.route('/project/<model("khmerrealty.type"):project_type>/<model("khmerrealty.project"):project_id>/',
                auth='public', website=True)
    def single_project(self, project_id, **kw):
        related_project = http.request.env['khmerrealty.project'].search([
            ('project_city', '=', project_id.project_city.id),
            ('id', '!=', project_id.id)], limit=4)
        return http.request.render('khmerrealty.project_single_page', {
            'project': project_id,
            'related_project': related_project,
            'banners': http.request.env['khmerrealty.advertising'].search([('show_in', '=', 'single_property')])
        })

    @http.route(['/agency/',
                 '/agency/page/<int:page>'], auth='public', website=True)
    def agency_list(self, page=1, **kw):
        agency_obj = request.env['res.partner']
        agency_count = agency_obj.search_count([('is_company', '=', True)])
        url = '/agency'
        pager = request.website.pager(url=url, total=agency_count, page=page,
                                      step=self._agency_per_page, scope=self._pager_step_ppg)
        return http.request.render('khmerrealty.agency-list-page', {
            'banners': http.request.env['khmerrealty.advertising'].search([('show_in', '=', 'property')], limit=3),
            'agency_obj': agency_obj.search([('is_company', '=', True)], limit=self._agency_per_page,
                                            offset=pager['offset']),
            'agency_count': agency_count,
            'pager': pager,
        })

    @http.route('/agency/<model("res.partner"):agency_id>', auth='public', website=True)
    def single_agency(self, agency_id, **kw):
        properties = request.env['khmerrealty.property'].search([('property_author.parent_id', '=', agency_id.id)])
        agents = request.env['res.partner'].search([('parent_id', '=', agency_id.id)])
        projects = request.env['khmerrealty.project'].search([('project_author.parent_id', '=', agency_id.id)])
        return http.request.render('khmerrealty.page-single-agency', {
            'agency': agency_id,
            'properties': properties,
            'agents': agents,
            'projects': projects,
        })

    @http.route(['/agent/<model("res.partner"):author_id>/',
                 '/agent/<model("res.partner"):author_id>/page/<int:page>'], auth='public', website=True)
    def property_by_author(self, author_id, page=1, **kw):
        properties = request.env['khmerrealty.property']
        property_count = properties.search_count([('property_author', '=', author_id.id)])
        if author_id:
            url = "/agent/%s" % slug(author_id)
        pager = request.website.pager(url=url, total=property_count, page=page,
                                      step=self._property_per_page, scope=self._pager_step_ppg)
        return http.request.render('khmerrealty.property_by_author', {
            'banners': http.request.env['khmerrealty.advertising'].search([('show_in', '=', 'property')], limit=3),
            'properties': properties.search([('property_author', '=', author_id.id)], limit=self._property_per_page,
                                            offset=pager['offset']),
            'author': author_id,
            'pager': pager,
        })

    @http.route(['/property/rent',
                 '/property/rent/page/<int:page>'], auth="public", website=True)
    def property_rent(self, page=1, **kw):
        property_obj = request.env['khmerrealty.property']
        property_type_obj = request.env['khmerrealty.type'].search([])
        property_count = property_obj.search_count([('property_category', '=', 'rent')])
        url = '/property/rent'
        property_type = 'rent'
        locations = request.env['khmerrealty.property.location'].search([('parent_id', '=', False)])
        pager = request.website.pager(url=url, total=property_count, page=page,
                                      step=self._property_per_page, scope=self._pager_step_ppg)
        properties = property_obj.search([('property_category', '=', 'rent')], limit=self._property_per_page,
                                         offset=pager['offset'])
        return http.request.render('khmerrealty.property_listing', {
            'banners': http.request.env['khmerrealty.advertising'].search([('show_in', '=', 'property')], limit=3),
            'properties': properties,
            'pager': pager,
            'property_type': property_type,
            'locations': locations,
            'property_type_obj': property_type_obj,
            'search_property_type': 'rent',
        })

    @http.route(['/property/buy',
                 '/property/buy/page/<int:page>'], auth="public", website=True)
    def property_buy(self, page=1, **kw):
        property_obj = request.env['khmerrealty.property']
        property_type_obj = request.env['khmerrealty.type'].search([])
        property_count = property_obj.search_count([('property_category', '=', 'buy')])
        url = '/property/buy'
        property_type = 'buy'
        locations = request.env['khmerrealty.property.location'].search([('parent_id', '=', False)])
        pager = request.website.pager(url=url, total=property_count, page=page,
                                      step=self._property_per_page, scope=self._pager_step_ppg)
        properties = property_obj.search([('property_category', '=', 'buy')], limit=self._property_per_page,
                                         offset=pager['offset'])
        return http.request.render('khmerrealty.property_listing', {
            'banners': http.request.env['khmerrealty.advertising'].search([('show_in', '=', 'property')], limit=3),
            'properties': properties,
            'pager': pager,
            'property_type': property_type,
            'locations': locations,
            'property_type_obj': property_type_obj,
            'search_property_type': 'buy',
        })

    @http.route(['/search/',
                 '/search/page/<int:page>'], auth='public', website=True)
    def search_property(self, page=1, search_value='', search_property_type='', ppg=False, **kw):
        search_table = 'khmerrealty.property'
        domain = []
        d_type = ['buy', 'rent']
        url = '/search'
        search_value = search_value.strip()
        record_obj = http.request.env[search_table]
        if ppg:
            try:
                ppg = int(ppg)
                kw['ppg'] = ppg
            except ValueError:
                ppg = False
        if search_property_type:
            kw['search_type'] = search_property_type
            if search_property_type in d_type:
                s_type = ('property_category', '=', search_property_type)
                domain.append(s_type)
        s_location = ('property_city', '=', int(kw['search_location']))
        domain.append(s_location)
        if search_value:
            kw['search_value'] = search_value
            for srch in search_value.split(" "):
                domain.append('|')
                sub_domain = ('name', 'ilike', srch)
                domain.append(sub_domain)
                des_s = ('description', 'ilike', srch)
                domain.append(des_s)
        record_count = record_obj.search_count(domain)
        pager = request.website.pager(url=url, total=record_count, page=page, step=self._property_search_page,
                                      scope=self._pager_step_ppg,
                                      url_args=kw)
        records = record_obj.search(domain, limit=self._property_search_page, offset=pager['offset'])
        locations = request.env['khmerrealty.property.location'].search([('parent_id', '=', False)])
        return http.request.render('khmerrealty.property_listing', {
            'search_location': int(kw.get('search_location')),
            'properties': records,
            'search_property_type': search_property_type,
            'pager': pager,
            'search_text': kw.get('search_text'),
            'locations': locations,
            'banners': http.request.env['khmerrealty.advertising'].search([('show_in', '=', 'property')], limit=3),
        })

    @http.route(['/property/type/<model("khmerrealty.type"):property_type_id>/',
                 '/property/type/<model("khmerrealty.type"):property_type_id>/page/<int:page>'], auth="public",
                website=True)
    def property_type(self, property_type_id, page=1, **kw):
        property_obj = request.env['khmerrealty.property']
        property_type_obj = request.env['khmerrealty.type'].search([])
        property_count = property_obj.search_count([('property_type', '=', property_type_id.id)])
        if property_type_id:
            url = '/property/type/%s' % slug(property_type_id)
        property_type = property_type_id.name
        locations = request.env['khmerrealty.property.location'].search([('parent_id', '=', False)])
        pager = request.website.pager(url=url, total=property_count, page=page,
                                      step=self._property_per_page, scope=self._pager_step_ppg)
        properties = property_obj.search([('property_type', '=', property_type_id.id)], limit=self._property_per_page,
                                         offset=pager['offset'])
        return http.request.render('khmerrealty.property_listing', {
            'banners': http.request.env['khmerrealty.advertising'].search([('show_in', '=', 'property')], limit=3),
            'properties': properties,
            'pager': pager,
            'property_type': property_type,
            'property_location': locations,
            'property_type_obj': property_type_obj,
        })

    @http.route(['/property-js/location/',
                 '/property-js/location/page/<int:page>'], auth='public', website=True)
    def property_filter_by_location(self, page=1, search_location_js='', ppg=False, **kw):
        search_table = 'khmerrealty.property'
        location_table = 'khmerrealty.property.location'
        domain = []
        url = '/property-js/location'
        record_obj = http.request.env[search_table]
        if ppg:
            try:
                ppg = int(ppg)
                kw['ppg'] = ppg
            except ValueError:
                ppg = False
        if search_location_js:
            kw['search_location_js'] = search_location_js
            location = ('property_city', '=', int(search_location_js))
            domain.append(location)
        record_count = record_obj.search_count(domain)
        pager = request.website.pager(url=url, total=record_count, page=page, step=self._property_search_page,
                                      scope=self._pager_step_ppg,
                                      url_args=kw)
        location_obj = http.request.env[location_table]
        records = record_obj.search(domain, limit=self._property_search_page, offset=pager['offset'])
        locations = location_obj.search([('parent_id', '=', False)])
        location_id = location_obj.search([('id', '=', int(search_location_js))])

        return http.request.render('khmerrealty.property_by_location', {
            'banners': http.request.env['khmerrealty.advertising'].search([('show_in', '=', 'property')], limit=3),
            'properties': records,
            'location': location_id,
            'property_location': locations,
            'pager': pager,
            'property_count': record_count,
        })
