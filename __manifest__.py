{
    'name': 'Max decuento ',
    'version': '1.0',
    'description': 'Restringir el descuento maximo en ventas por categoria',
    'author': 'Yostin Palacios Calle',
    'website': 'https://example.com',
    'license': 'LGPL-3',
    'category': 'sale',
    'depends': [
        'base', 'sale', 'product'
    ],
    'data': [
        'security/security.xml',
        'view/product-inherit.xml',
    ],
    'auto_install': False,
    'application': False,
}