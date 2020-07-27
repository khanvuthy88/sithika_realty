# -*- coding: utf-8 -*-
{
    'name': "khmerrealty",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'website', 'website_blog', 'contacts', 'portal'],

    # always loaded
    'data': [
        'security/property_security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/project_views.xml',
        'views/res_partner_views.xml',
        'views/ads_views.xml',
        'views/slide.xml',
        'views/assets.xml',
        'views/new_template.xml',
        'views/templates.xml',
        'views/website_blog.xml',
        'views/res_group.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}