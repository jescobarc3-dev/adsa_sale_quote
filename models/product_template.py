from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Identificación en propuesta
    adsa_quote_status = fields.Selection([
        ('ok', 'Implementado'),
        ('wip', 'En Implementación'),
        ('svc', 'Servicio Continuo'),
    ], string='Estado en propuesta ADSA', default='wip')

    adsa_quote_layout = fields.Selection([
        ('A', 'Layout A — Estado + 3 columnas'),
        ('B', 'Layout B — Grid 2×2'),
    ], string='Layout de página de módulo', help='Si está vacío, el producto no genera página de módulo.')

    adsa_quote_icon = fields.Selection([
        ('ticket', 'Ticket'),
        ('truck', 'Camión / Flotillas'),
        ('cloud', 'Nube / Soporte'),
        ('building', 'Edificio'),
        ('gear', 'Engranaje'),
        ('chart', 'Gráfica'),
        ('shield', 'Escudo'),
        ('rocket', 'Cohete'),
        ('users', 'Usuarios'),
        ('server', 'Servidor'),
        ('dollar', 'Dinero'),
        ('puzzle', 'Puzzle'),
        ('link', 'Enlace'),
    ], string='Ícono en propuesta', default='gear')

    # Página de solución (p3)
    adsa_quote_num = fields.Char(string='Número en solución', default='01', help='01, 02, 03...')
    adsa_quote_subtitle = fields.Char(string='Subtítulo de módulo', help='Descripción corta bajo el nombre')
    adsa_quote_feature_ids = fields.One2many(
        'adsa.quote.feature', 'product_tmpl_id', string='Características (solución p3)')

    # Imagen para solución — si vacío usa image_1920
    adsa_quote_sol_image = fields.Image(string='Imagen para página de solución', max_width=400, max_height=400)

    # Página de módulo — datos comunes
    adsa_quote_header_sub = fields.Char(string='Subtítulo del header de página')

    # Layout A
    adsa_quote_state_title = fields.Char(string='[A] Título del estado', default='Estado actual')
    adsa_quote_state_text = fields.Text(string='[A] Descripción del estado')
    adsa_quote_col_ids = fields.One2many(
        'adsa.quote.module.col', 'product_tmpl_id', string='[A] Columnas de módulo')
    adsa_quote_note = fields.Char(string='[A] Nota inferior')

    # Layout B
    adsa_quote_scope_items = fields.Text(string='[B] Alcance funcional', help='Un ítem por línea')
    adsa_quote_rules_items = fields.Text(string='[B] Reglas operativas', help='Un ítem por línea')
    adsa_quote_bridge_replaces = fields.Char(string='[B] Qué reemplaza')
    adsa_quote_bridge_eliminates = fields.Char(string='[B] Qué evita')
    adsa_quote_bridge_controls = fields.Char(string='[B] Qué controla')
    adsa_quote_sap_note = fields.Text(string='[B] Nota de integración SAP')

    # Página de perfiles
    adsa_quote_profile_ids = fields.One2many(
        'adsa.quote.profile', 'product_tmpl_id', string='Perfiles de usuario')

    # Página económica
    adsa_quote_monthly_amount = fields.Char(string='Monto mensual', default='Q0.00 / mes')
    adsa_quote_monthly_notes = fields.Text(string='Notas adicionales del monto', help='Una nota por línea')

    def get_scope_list(self):
        return [i.strip() for i in (self.adsa_quote_scope_items or '').splitlines() if i.strip()]

    def get_rules_list(self):
        return [i.strip() for i in (self.adsa_quote_rules_items or '').splitlines() if i.strip()]

    def get_monthly_notes(self):
        return [i.strip() for i in (self.adsa_quote_monthly_notes or '').splitlines() if i.strip()]
