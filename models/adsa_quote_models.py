from odoo import models, fields


class AdsaQuoteContextPoint(models.Model):
    _name = 'adsa.quote.context.point'
    _description = 'Punto de contexto en propuesta ADSA'
    _order = 'sequence, id'

    order_id = fields.Many2one('sale.order', required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)
    title = fields.Char(required=True)
    icon = fields.Selection([
        ('building', 'Edificio'),
        ('chart', 'Gráfica'),
        ('warning', 'Advertencia'),
        ('cost', 'Costo'),
        ('check', 'Check'),
        ('info', 'Info'),
        ('shield', 'Escudo'),
        ('rocket', 'Cohete'),
        ('gear', 'Engranaje'),
        ('truck', 'Camión'),
        ('cloud', 'Nube'),
        ('ticket', 'Ticket'),
    ], default='info')
    items = fields.Text(help='Un ítem por línea')
    badge = fields.Selection([
        ('ok', 'Implementado'),
        ('wip', 'En Implementación'),
        ('svc', 'Servicio Continuo'),
        ('', 'Sin badge'),
    ], default='')

    def get_items_list(self):
        return [i.strip() for i in (self.items or '').splitlines() if i.strip()]


class AdsaQuoteTimelineStep(models.Model):
    _name = 'adsa.quote.timeline.step'
    _description = 'Paso del cronograma en propuesta ADSA'
    _order = 'sequence, id'

    order_id = fields.Many2one('sale.order', required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)
    title = fields.Char(required=True)
    description = fields.Char()


class AdsaQuoteModuleCol(models.Model):
    _name = 'adsa.quote.module.col'
    _description = 'Columna de módulo Layout A'
    _order = 'sequence, id'

    product_tmpl_id = fields.Many2one('product.template', required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)
    title = fields.Char(required=True)
    icon = fields.Selection([
        ('check', 'Check'),
        ('chart', 'Gráfica'),
        ('rocket', 'Cohete'),
        ('gear', 'Engranaje'),
        ('shield', 'Escudo'),
        ('info', 'Info'),
        ('users', 'Usuarios'),
    ], default='check')
    items = fields.Text(help='Un ítem por línea (si es lista)')
    text_content = fields.Text(help='Párrafo (si no es lista)')

    def get_items_list(self):
        return [i.strip() for i in (self.items or '').splitlines() if i.strip()]


class AdsaQuoteProfile(models.Model):
    _name = 'adsa.quote.profile'
    _description = 'Perfil de usuario en propuesta ADSA'
    _order = 'sequence, id'

    product_tmpl_id = fields.Many2one('product.template', required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)
    profile_name = fields.Char(string='Perfil', required=True)
    functions = fields.Char(string='Funciones principales', required=True)
    access = fields.Selection([
        ('Completo', 'Completo'),
        ('Intermedio', 'Intermedio'),
        ('Limitado', 'Limitado'),
    ], default='Completo', required=True)


class AdsaQuoteFeature(models.Model):
    _name = 'adsa.quote.feature'
    _description = 'Característica de módulo en propuesta ADSA'
    _order = 'sequence, id'

    product_tmpl_id = fields.Many2one('product.template', required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)
    name = fields.Char(required=True)
