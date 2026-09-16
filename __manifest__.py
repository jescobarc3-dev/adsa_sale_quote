{
    'name': 'ADSA — Propuesta Comercial Premium',
    'version': '19.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Reporte PDF premium de propuesta comercial para clientes ADSA',
    'author': 'ADSA / Asesoría Digital S.A.',
    'license': 'LGPL-3',
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/paperformat.xml',
        'views/product_template_views.xml',
        'views/sale_order_views.xml',
        'report/report_adsa_quote.xml',
    ],
    'assets': {
        'web.report_assets_common': [
            'adsa_sale_quote/static/src/css/adsa_quote.css',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
