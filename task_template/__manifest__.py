# -*- coding: utf-8 -*-
{
    'name': "SIT -  Task template",

    'summary': """
        Module that add a task template""",

    'description': """
        Long description of module's purpose
    """,

    'author': "SimplicIT",
    'website': "https://www.simplicit.pro",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Project',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_timesheet', 'product', 'project', 'sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/task_template_views.xml',
        'views/product_views.xml',
    ],
}
