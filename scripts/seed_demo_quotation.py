#!/usr/bin/env python3
"""
seed_demo_quotation.py
======================
Inserta la cotización demo de ADSA (Protección Total, S.A.) en Odoo 19
vía XML-RPC. Replica exactamente el objeto P de cotizacion.html.

Uso:
    python3 seed_demo_quotation.py \
        --url https://360.adsa.com.gt \
        --db <nombre_base_datos> \
        --user admin \
        --password <tu_password>
"""

import xmlrpc.client
import argparse
import sys

# ── Argumentos ────────────────────────────────────────────────────────────────
parser = argparse.ArgumentParser(description='Seed ADSA demo quotation into Odoo 19')
parser.add_argument('--url',      default='https://360.adsa.com.gt')
parser.add_argument('--db',       required=True, help='Nombre de la base de datos Odoo')
parser.add_argument('--user',     default='admin')
parser.add_argument('--password', required=True)
args = parser.parse_args()

URL  = args.url.rstrip('/')
DB   = args.db
USER = args.user
PASS = args.password

# ── Conexión XML-RPC ──────────────────────────────────────────────────────────
print(f'Conectando a {URL} ...')
common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
uid    = common.authenticate(DB, USER, PASS, {})
if not uid:
    print('ERROR: Autenticación fallida. Verifica usuario y contraseña.')
    sys.exit(1)
print(f'Autenticado como uid={uid}')

models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')

def call(model, method, *args, **kwargs):
    return models.execute_kw(DB, uid, PASS, model, method, list(args), kwargs)

def find_or_create(model, domain, vals):
    ids = call(model, 'search', domain)
    if ids:
        return ids[0]
    return call(model, 'create', vals)

# ══════════════════════════════════════════════════════════════════════════════
# 1. PARTNER — Protección Total, S.A.
# ══════════════════════════════════════════════════════════════════════════════
print('\n[1/6] Creando/buscando cliente...')
partner_id = find_or_create(
    'res.partner',
    [('name', '=', 'Protección Total, S.A.')],
    {'name': 'Protección Total, S.A.', 'is_company': True, 'customer_rank': 1}
)
print(f'  Partner id={partner_id}')

# ══════════════════════════════════════════════════════════════════════════════
# 2. PRODUCTOS / MÓDULOS
# ══════════════════════════════════════════════════════════════════════════════
print('\n[2/6] Creando productos...')

# ── Producto 1: Tickets + Encuestas (Layout A, status: ok) ──────────────────
prod1_id = find_or_create(
    'product.template',
    [('name', '=', 'Tickets + Encuestas')],
    {
        'name':                     'Tickets + Encuestas',
        'type':                     'service',
        'list_price':               1000.0,
        'adsa_quote_status':        'ok',
        'adsa_quote_layout':        'A',
        'adsa_quote_icon':          'ticket',
        'adsa_quote_num':           '01',
        'adsa_quote_subtitle':      'Mesa de ayuda y retroalimentación en tiempo real',
        'adsa_quote_header_sub':    'Resultado entregado y operando',
        'adsa_quote_state_title':   'Estado actual',
        'adsa_quote_state_text':    (
            'ADSA ya implementó y dejó operando el módulo de Tickets + Encuestas '
            'para Protección Total. El cliente cuenta con una base funcional para '
            'registrar solicitudes, dar seguimiento y medir satisfacción.'
        ),
        'adsa_quote_note':          'Incluye app Android (APK) para operación de tickets en hasta 5 dispositivos.',
        'adsa_quote_monthly_amount':'Q1,000.00 / mes',
    }
)
print(f'  Producto 1 (Tickets + Encuestas) id={prod1_id}')

# Eliminar relaciones existentes antes de recrear
call('adsa.quote.feature',    'unlink', call('adsa.quote.feature',    'search', [('product_tmpl_id','=',prod1_id)]))
call('adsa.quote.module.col', 'unlink', call('adsa.quote.module.col', 'search', [('product_tmpl_id','=',prod1_id)]))
call('adsa.quote.profile',    'unlink', call('adsa.quote.profile',    'search', [('product_tmpl_id','=',prod1_id)]))

# Features (bullets en p3)
for seq, feat in enumerate([
    'Gestión de turnos por área (RH y Operaciones)',
    'Encuestas de satisfacción post-servicio',
    'Operación en tablets Android',
], start=10):
    call('adsa.quote.feature', 'create', {
        'product_tmpl_id': prod1_id,
        'sequence': seq,
        'name': feat,
    })

# Columnas Layout A
cols_a1 = [
    ('Qué está funcionando',        'check',  'Registro de solicitudes\nSeguimiento de solicitudes\nFlujo de atención\nEncuestas de satisfacción', None),
    ('Resultado comercial',          'chart',  None, 'Este módulo es una demostración de cumplimiento y capacidad de ejecución. La continuidad propuesta parte de una entrega real, no de una promesa.'),
    ('Valor para la siguiente fase', 'rocket', None, 'La experiencia ya ganada reduce fricción, acelera decisiones y facilita la expansión hacia Inventario + Flotillas.'),
]
for seq, (title, icon, items, text) in enumerate(cols_a1, start=10):
    call('adsa.quote.module.col', 'create', {
        'product_tmpl_id': prod1_id,
        'sequence':     seq,
        'title':        title,
        'icon':         icon,
        'items':        items or '',
        'text_content': text  or '',
    })

# Perfiles de acceso
for seq, (prof, func, access) in enumerate([
    ('Agente de Soporte',   'Gestión de tickets, seguimiento y resolución.',      'Completo'),
    ('Usuario Solicitante', 'Crea tickets y responde encuestas de satisfacción.', 'Limitado'),
], start=10):
    call('adsa.quote.profile', 'create', {
        'product_tmpl_id': prod1_id,
        'sequence': seq,
        'profile_name': prof,
        'functions':    func,
        'access':       access,
    })

# ── Producto 2: Inventario + Flotillas (Layout B, status: wip) ──────────────
prod2_id = find_or_create(
    'product.template',
    [('name', '=', 'Inventario + Flotillas')],
    {
        'name':  'Inventario + Flotillas',
        'type':  'service',
        'list_price': 1000.0,
    }
)
call('product.template', 'write', [prod2_id], {
    'adsa_quote_status':         'wip',
    'adsa_quote_layout':         'B',
    'adsa_quote_icon':           'truck',
    'adsa_quote_num':            '02',
    'adsa_quote_subtitle':       'Control total de activos y operación en campo',
    'adsa_quote_header_sub':     'Fase actual de implementación',
    'adsa_quote_scope_items':    (
        'Control de existencias por almacén\n'
        'Registro de ingresos, salidas y ajustes\n'
        'Catálogo maestro de vehículos\n'
        'Órdenes de servicio preventivo y correctivo\n'
        'Control de insumos por orden de servicio\n'
        'Trazabilidad de consumos por vehículo'
    ),
    'adsa_quote_rules_items':    (
        'Movimientos registrados por usuario responsable\n'
        'Trazabilidad por almacén y documento\n'
        'Control por vehículo, insumo y orden\n'
        'Catálogos homologados con SAP'
    ),
    'adsa_quote_bridge_replaces':   'Controles manuales dispersos y seguimiento no centralizado.',
    'adsa_quote_bridge_eliminates': 'Retrabajo, diferencias de inventario, consumos sin soporte y poca visibilidad de costos.',
    'adsa_quote_bridge_controls':   'Existencias, movimientos, vehículos, órdenes de servicio e insumos por unidad.',
    'adsa_quote_sap_note':          (
        'ADSA desarrollará un addon de importación en Odoo para recibir existencias '
        'exportadas desde SAP, manteniendo la homologación entre sistemas y la '
        'consistencia operativa.'
    ),
    'adsa_quote_monthly_amount':    'Q1,000.00 / mes',
})
print(f'  Producto 2 (Inventario + Flotillas) id={prod2_id}')

call('adsa.quote.feature',    'unlink', call('adsa.quote.feature',    'search', [('product_tmpl_id','=',prod2_id)]))
call('adsa.quote.profile',    'unlink', call('adsa.quote.profile',    'search', [('product_tmpl_id','=',prod2_id)]))

for seq, feat in enumerate([
    'Gestión unificada de inventario',
    'Control de flotas (preventivo y correctivo)',
    'Integración con SAP (existencias)',
], start=10):
    call('adsa.quote.feature', 'create', {'product_tmpl_id': prod2_id, 'sequence': seq, 'name': feat})

for seq, (prof, func, access) in enumerate([
    ('Almacén / Inventario', 'Recepciones, existencias, salidas, ajustes y reportería.',               'Completo'),
    ('Flota Operativa',      'Catálogo vehicular, órdenes de servicio, insumos y recorridos.',         'Completo'),
    ('Flota Supervisor',     'Consulta costos e historial, valida servicios.',                          'Intermedio'),
], start=10):
    call('adsa.quote.profile', 'create', {'product_tmpl_id': prod2_id, 'sequence': seq,
                                           'profile_name': prof, 'functions': func, 'access': access})

# ── Producto 3: Soporte + Backups + Nube ADSA (sin layout, solo solución) ───
prod3_id = find_or_create(
    'product.template',
    [('name', '=', 'Soporte + Backups + Nube privada ADSA')],
    {'name': 'Soporte + Backups + Nube privada ADSA', 'type': 'service', 'list_price': 1000.0}
)
call('product.template', 'write', [prod3_id], {
    'adsa_quote_status':        'svc',
    'adsa_quote_layout':        False,   # sin página de detalle propia
    'adsa_quote_icon':          'cloud',
    'adsa_quote_num':           '03',
    'adsa_quote_subtitle':      'Tu operación siempre segura y disponible',
    'adsa_quote_monthly_amount':'Q1,000.00 / mes',
    'adsa_quote_monthly_notes': 'Incluye bolsa de 15 a 20 horas mensuales.\nUso flexible según necesidad.',
})
print(f'  Producto 3 (Soporte + Backups + Nube ADSA) id={prod3_id}')

call('adsa.quote.feature', 'unlink', call('adsa.quote.feature', 'search', [('product_tmpl_id','=',prod3_id)]))
call('adsa.quote.profile', 'unlink', call('adsa.quote.profile', 'search', [('product_tmpl_id','=',prod3_id)]))

for seq, feat in enumerate([
    'Soporte técnico especializado 15-20 hrs/mes',
    'Respaldos automáticos y monitoreo',
    'Alta disponibilidad y seguridad',
], start=10):
    call('adsa.quote.feature', 'create', {'product_tmpl_id': prod3_id, 'sequence': seq, 'name': feat})

for seq, (prof, func, access) in enumerate([
    ('Usuario ADSA',          'Soporte activo y resolución.',                                    'Completo'),
    ('Administrador Cliente', 'Puede agregar usuarios y realizar configuración básica.',          'Intermedio'),
    ('Soporte ADSA',          'Administración de plataforma, respaldos y monitoreo.',             'Completo'),
], start=10):
    call('adsa.quote.profile', 'create', {'product_tmpl_id': prod3_id, 'sequence': seq,
                                           'profile_name': prof, 'functions': func, 'access': access})

# Obtener product.product ids para las líneas de pedido
def get_product_id(tmpl_id):
    ids = call('product.product', 'search', [('product_tmpl_id', '=', tmpl_id)])
    return ids[0] if ids else None

pp1 = get_product_id(prod1_id)
pp2 = get_product_id(prod2_id)
pp3 = get_product_id(prod3_id)

# ══════════════════════════════════════════════════════════════════════════════
# 3. SALE ORDER — Cotización PT-2026-001
# ══════════════════════════════════════════════════════════════════════════════
print('\n[3/6] Creando cotización...')

order_id = call('sale.order', 'create', {
    'partner_id':   partner_id,
    'client_order_ref': 'PT-2026-001',

    # ── Portada ──
    'adsa_cover_title':   'Continuidad de la transformación',
    'adsa_cover_accent':  'operativa',
    'adsa_cover_sub1':    'Siguiente fase: Inventario + Flotillas',
    'adsa_cover_sub2':    'sobre una base ya entregada y operando',

    # ── Contexto ──
    'adsa_context_title':    'Contexto actual y avance comprobado',
    'adsa_context_subtitle': 'Base ya entregada y oportunidad de consolidación',
    'adsa_context_why': (
        'Porque ya conocemos tu entorno, ya te apoyamos y ya operamos una primera fase. '
        'La siguiente propuesta parte de cero a cero y se construye sobre resultados '
        'sobre una base comprobada.'
    ),
    'adsa_context_proof': 'Prueba de cumplimiento',

    # ── Solución ──
    'adsa_solution_title':  'Una solución integral,',
    'adsa_solution_accent': 'enfocada en tus necesidades',
    'adsa_solution_desc': (
        'En ADSA unimos tecnología, experiencia y acompañamiento para brindar a '
        'Protección Total una solución integral que digitaliza procesos clave, mejora '
        'la eficiencia operativa y garantiza la continuidad del servicio.'
    ),
    'adsa_solution_ally': (
        'Te acompañamos en cada etapa, desde la implementación hasta la operación '
        'continua, con un enfoque práctico y orientado a resultados.'
    ),

    # ── Perfiles ──
    'adsa_profiles_title':    'Perfiles y alcance operativo',
    'adsa_profiles_subtitle': 'Perfiles de referencia por línea de servicio',
    'adsa_profiles_model': (
        'La propuesta se define como un servicio gestionado integral con capacidad base '
        'incluida por módulo. Usuarios o dispositivos adicionales: Q100 por usuario o '
        'dispositivo. Las ampliaciones de capacidad se notifican siempre al inicio del período.'
    ),

    # ── Económico ──
    'adsa_economic_title':    'Resumen económico',
    'adsa_economic_subtitle': 'Servicio gestionado con valor operativo',
    'adsa_economic_intro': (
        'La propuesta se presenta como un servicio gestionado integral con capacidad base '
        'incluida por módulo: una fase ya entregada, una fase actual de implementación y '
        'una capa continua de soporte, respaldos y nube privada.'
    ),
    'adsa_onetime_name':   'Implementación de la fase Inventario + Flotillas',
    'adsa_onetime_desc': (
        'Incluye carga de catálogos, adecuación de campos para homologación con SAP '
        'y desarrollo de addon de importación en Odoo.'
    ),
    'adsa_onetime_amount':    'Q1,300.00',
    'adsa_economic_note': (
        'Inventario + Flotillas incluye hasta 10 usuarios. Tickets + Encuestas incluye '
        'base de hasta 5 dispositivos/App. Usuarios o dispositivos adicionales: Q100. '
        'La implementación actual corresponde a Inventario + Flotillas.'
    ),

    # ── Cierre ──
    'adsa_closure_title':    'Cierre y próximos pasos',
    'adsa_closure_subtitle': 'Ruta clara para activar la siguiente fase',
    'adsa_validity_text':    '15 días calendario a partir de la fecha de emisión.',
    'adsa_closure_message': (
        'ADSA ya entregó una fase operativa. Esta propuesta permite capitalizar ese '
        'avance y consolidar el siguiente paso con control, trazabilidad y continuidad.'
    ),
    'adsa_next_steps': (
        'Aprobación comercial\n'
        'Programación de kickoff\n'
        'Entrega de insumos y catálogos\n'
        'Inicio de implementación'
    ),

    # ── Contactos footer ──
    'adsa_contact1_name':  'José Escobar',
    'adsa_contact1_phone': '51951605',
    'adsa_contact2_name':  'Pedro Tay',
    'adsa_contact2_phone': '51381308',

    # ── Líneas de pedido ──
    'order_line': [
        (0, 0, {
            'product_id':    pp1,
            'name':          'Tickets + Encuestas',
            'product_uom_qty': 1,
            'price_unit':    1000.0,
        }),
        (0, 0, {
            'product_id':    pp2,
            'name':          'Inventario + Flotillas',
            'product_uom_qty': 1,
            'price_unit':    1000.0,
        }),
        (0, 0, {
            'product_id':    pp3,
            'name':          'Soporte + Backups + Nube privada ADSA',
            'product_uom_qty': 1,
            'price_unit':    1000.0,
        }),
    ],
})
print(f'  Sale order id={order_id}')

# ══════════════════════════════════════════════════════════════════════════════
# 4. PUNTOS DE CONTEXTO (página 2)
# ══════════════════════════════════════════════════════════════════════════════
print('\n[4/6] Creando puntos de contexto...')

context_points = [
    ('Situación actual', 'building', 'ok', [
        'Gestión centralizada de tickets',
        'Seguimiento de solicitudes',
        'Encuestas de satisfacción',
        'Operación activa y validada',
    ]),
    ('Lo ya logrado con ADSA', 'chart', 'ok', [
        'Gestión centralizada de tickets',
        'Seguimiento de solicitudes',
        'Encuestas de satisfacción',
        'Operación activa y validada',
    ]),
    ('Brecha que aún existe', 'warning', '', [
        'Inventario y flotas todavía requieren control centralizado.',
        'Trazabilidad operativa insuficiente.',
        'Fiabilidad limitada para la toma de decisiones.',
    ]),
    ('Costo de no avanzar', 'cost', '', [
        'Salidas e ingresos sin trazabilidad suficiente.',
        'Difícil controlar consumos por vehículo.',
        'Menor visibilidad de existencias y costos.',
        'Riesgo en licitaciones tardías.',
    ]),
]

for seq, (title, icon, badge, items) in enumerate(context_points, start=10):
    call('adsa.quote.context.point', 'create', {
        'order_id':  order_id,
        'sequence':  seq,
        'title':     title,
        'icon':      icon,
        'badge':     badge,
        'items':     '\n'.join(items),
    })
    print(f'  Punto: {title}')

# ══════════════════════════════════════════════════════════════════════════════
# 5. CRONOGRAMA (página de cierre)
# ══════════════════════════════════════════════════════════════════════════════
print('\n[5/6] Creando cronograma...')

timeline = [
    ('Levantamiento y homologación SAP',
     'Definición de campos, estructura de catálogos y criterios de integración.'),
    ('Carga y programación',
     'Carga inicial de catálogos y parametrización de Inventario + Flotillas.'),
    ('Pruebas y validación',
     'Pruebas funcionales, validación operativa y ajustes finales.'),
    ('Salida controlada',
     'Puesta en marcha, acompañamiento y monitoreo.'),
]

for seq, (title, desc) in enumerate(timeline, start=10):
    call('adsa.quote.timeline.step', 'create', {
        'order_id':    order_id,
        'sequence':    seq,
        'title':       title,
        'description': desc,
    })
    print(f'  Paso: {title}')

# ══════════════════════════════════════════════════════════════════════════════
# 6. RESULTADO
# ══════════════════════════════════════════════════════════════════════════════
order_data = call('sale.order', 'read', [order_id], fields=['name'])[0]
print(f'\n✅ Cotización creada: {order_data["name"]} (id={order_id})')
print(f'\nAbre en Odoo:')
print(f'  {URL}/odoo/sales/{order_id}')
print(f'\nLuego: Imprimir → Propuesta Comercial ADSA')
