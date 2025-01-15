from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleDescuento(models.Model):
    _inherit = 'sale.order'

    def write(self, vals):
        res = super(SaleDescuento, self).write(vals)
        # Verifica si hay cambios en las líneas de pedido
        if 'order_line' in vals:
            self.max_descuento()
            self.update_price_product()  # Asegúrate de ejecutar la actualización después de los cambios
        return res

    def create(self, vals):
        res = super(SaleDescuento, self).create(vals)
        if 'order_line' in vals:
            self.max_descuento()
            self.update_price_product()  # Asegúrate de ejecutar la actualización después de los cambios
        return res

    def max_descuento(self):
        for record in self:
            if self.env.user.has_group('max_descuento.group_user_ventas'):
                for line in record.order_line:
                    descuento_max = line.product_template_id.categ_id.descuento_max or line.product_template_id.categ_id.parent_id.descuento_max
                    if line.discount > descuento_max:
                        raise UserError(
                            f"El descuento {line.discount}% del producto '{line.product_id.name}' excede el "
                            f"descuento máximo permitido en la categoría '{line.product_template_id.categ_id.name}'."
                        )

    @api.depends('order_line.product_template_id')          
    def update_price_product(self):
        for record in self:
            if self.env.user.has_group('max_descuento.group_user_ventas'):
                for line in record.order_line:
                    
                    # Verifica si el producto es un producto (no un servicio) y si el precio de lista es igual al precio unitario
                    if line.product_template_id.detailed_type == 'product':
                        if line.price_unit != line.product_template_id.list_price:
                            # Si el precio unitario no es igual al precio de lista y el producto es nuevo, no se modifica
                            precio = round(line.price_unit, 2) 
                            if line.id and precio != line.product_template_id.list_price:
                                raise UserError(
                                    f"Usted no tiene permitido cambiar el precio establecido en el producto '{line.product_id.name}' "
                                    f"al precio de lista de '{line.product_template_id.list_price}'."
                                )
                            line.write({
                                'price_unit': line.product_template_id.list_price
                            })
