from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # ── PORTADA ──────────────────────────────────────────────────────────────
    adsa_cover_title = fields.Char(string='Título portada', default='Propuesta comercial')
    adsa_cover_accent = fields.Char(string='Acento portada (cyan)', default='ADSA')
    adsa_cover_sub1 = fields.Char(string='Subtítulo portada (tag)')
    adsa_cover_sub2 = fields.Char(string='Descripción portada')

    # ── CONTEXTO (p2) ─────────────────────────────────────────────────────────
    adsa_context_title = fields.Char(string='Título contexto', default='Contexto actual y avance comprobado')
    adsa_context_subtitle = fields.Char(string='Subtítulo contexto', default='Situación actual y oportunidad')
    adsa_context_point_ids = fields.One2many(
        'adsa.quote.context.point', 'order_id', string='Puntos de contexto')
    adsa_context_why = fields.Text(string='¿Por qué ADSA?')
    adsa_context_proof = fields.Char(string='Etiqueta de prueba', default='Prueba de cumplimiento')

    # ── SOLUCIÓN (p3) ─────────────────────────────────────────────────────────
    adsa_solution_title = fields.Char(string='Título solución', default='Una solución integral,')
    adsa_solution_accent = fields.Char(string='Acento título solución', default='enfocada en tus necesidades')
    adsa_solution_desc = fields.Text(string='Descripción solución')
    adsa_solution_ally = fields.Text(string='Texto aliado estratégico')

    # ── PERFILES (página variable) ────────────────────────────────────────────
    adsa_profiles_title = fields.Char(string='Título perfiles', default='Perfiles y alcance operativo')
    adsa_profiles_subtitle = fields.Char(string='Subtítulo perfiles', default='Perfiles de referencia por línea de servicio')
    adsa_profiles_model = fields.Text(string='Modelo de dimensionamiento',
        default='La propuesta se define como un servicio gestionado integral con capacidad base incluida por módulo.')

    # ── ECONÓMICO ─────────────────────────────────────────────────────────────
    adsa_economic_title = fields.Char(string='Título económico', default='Resumen económico')
    adsa_economic_subtitle = fields.Char(string='Subtítulo económico', default='Servicio gestionado con valor operativo')
    adsa_economic_intro = fields.Text(string='Intro económico')
    adsa_economic_note = fields.Text(string='Nota económica')

    # ── CIERRE ────────────────────────────────────────────────────────────────
    adsa_closure_title = fields.Char(string='Título cierre', default='Cierre y próximos pasos')
    adsa_closure_subtitle = fields.Char(string='Subtítulo cierre', default='Ruta clara para activar la siguiente fase')
    adsa_timeline_ids = fields.One2many(
        'adsa.quote.timeline.step', 'order_id', string='Cronograma')
    adsa_next_steps = fields.Text(string='Próximos pasos', help='Un paso por línea')
    adsa_validity_text = fields.Char(string='Vigencia', default='15 días calendario a partir de la fecha de emisión.')
    adsa_closure_message = fields.Text(string='Mensaje de cierre')

    # Contactos en footer última página
    adsa_contact1_name = fields.Char(string='Contacto 1 — Nombre')
    adsa_contact1_phone = fields.Char(string='Contacto 1 — Teléfono')
    adsa_contact2_name = fields.Char(string='Contacto 2 — Nombre')
    adsa_contact2_phone = fields.Char(string='Contacto 2 — Teléfono')

    def adsa_module_lines(self):
        """Líneas de pedido cuyo producto tiene layout de módulo configurado."""
        return self.order_line.filtered(
            lambda l: not l.display_type
            and l.product_id.product_tmpl_id.adsa_quote_layout
        )

    def adsa_recurring_lines(self):
        """Todas las líneas que NO son pago único — tabla económica y página de solución."""
        return self.order_line.filtered(
            lambda l: not l.display_type
            and l.product_id.product_tmpl_id.adsa_quote_billing_type != 'onetime'
        )

    def adsa_solution_lines(self):
        """Las primeras 3 líneas recurrentes (para página de solución p3)."""
        return self.adsa_recurring_lines()[:3]

    def adsa_onetime_lines(self):
        """Líneas de pago único/implementación — card naranja en página económica."""
        return self.order_line.filtered(
            lambda l: not l.display_type
            and l.product_id.product_tmpl_id.adsa_quote_billing_type == 'onetime'
        )

    def adsa_next_steps_list(self):
        return [s.strip() for s in (self.adsa_next_steps or '').splitlines() if s.strip()]

    def adsa_total_pages(self):
        """Número total de páginas: 4 fijas + módulos + 2 fijas."""
        return 4 + len(self.adsa_module_lines()) + 2

    def adsa_contacts(self):
        contacts = []
        if self.adsa_contact1_name and self.adsa_contact1_phone:
            contacts.append({'name': self.adsa_contact1_name, 'phone': self.adsa_contact1_phone})
        if self.adsa_contact2_name and self.adsa_contact2_phone:
            contacts.append({'name': self.adsa_contact2_name, 'phone': self.adsa_contact2_phone})
        return contacts

    def action_print_adsa_quote(self):
        return self.env.ref('adsa_sale_quote.action_report_adsa_sale_quote').report_action(self)
