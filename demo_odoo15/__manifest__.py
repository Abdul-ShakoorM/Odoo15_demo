# -*- coding: utf-8 -*-
{
    'name': "demo_odoo15",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "AS",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Productivity',
    'version': '0.1',
    'sequence': -100,
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/sequence_data.xml',
        'wizard/create_appointment_view.xml',
        'views/patient.xml',
        'views/doctor.xml',
        'views/appointment.xml',
        'views/sale.xml',
        'views/partner.xml',
        'reports/report.xml',
        'reports/custom_header_footer.xml',
        'reports/report_patient_card.xml',
        'reports/report_patient_detail.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'qweb': [
        # 'static/src/xml/button.xml',
    ]
}
