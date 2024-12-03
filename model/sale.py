from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleDescuento(models.Model):
    _inherit = 'sale.order'

    def write(self, vals):
        res = super(SaleDescuento, self).write(vals)
        # Verifica si hay cambios en las líneas de pedido
        if 'order_line' in vals:
            print('----------------------------------------------------------')
            print('EJECUCION DE LA FUNCION DE MAXIMO DESCUENTO')
            self.max_descuento()
        return res

    def max_descuento(self):
        for record in self:
            # print('----------------------------------------------------------')
            # print('EJECUCION DE LA FUNCION DE MAXIMO DESCUENTO')
            # Verificar si el usuario pertenece al grupo específico
            if self.env.user.has_group('max_descuento.group_user_ventas'):
                for line in record.order_line:
                    if line.discount > line.product_template_id.categ_id.descuento_max:
                        raise UserError(
                            f"El descuento {line.discount}% del producto '{line.product_id.name}' excede el "
                            f"descuento máximo permitido en la categoría '{line.product_template_id.categ_id.name}'."
                        )
