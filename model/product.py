from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError


class DescuentoProduct(models.Model):
    _inherit = 'product.category'

    descuento_max = fields.Float(string="Descuento Máximo (%)", group="max_descuento.group_user_ventas")
