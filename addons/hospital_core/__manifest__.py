# -*- coding: utf-8 -*-
{
    'name': 'Hospital Core',
    'version': '1.0',
    'summary': 'Système minimal hospitalier: planning, patients, RDV, actes',
    'category': 'Healthcare',
    'author': 'TonNom',
    'license': 'LGPL-3',
    'depends': ['base', 'mail', 'account'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/menus.xml',         # Chargé en premier pour les actions
        'security/ir_rule.xml',
        'views/patient_views.xml',
        'views/appointment_views.xml',
        'views/planning_views.xml',
    ],
    'installable': True,
    'application': True,
}