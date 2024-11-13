{
    "name": "Equipment Maintenance",
    "version": "16.0.1.0.0",
    "author": "Fouad Bittar",
    "website": "https://github.com/FouadB1990",
    "category": "Maintenance",
    "complexity": "easy",
    'license': 'LGPL-3',
    'summary': """
        Equipment Maintenance Custom Module.""",
    "description": """
        Equipment Maintenance Custom Module.
    """,
    'depends': ['base','product','maintenance'],
    "data": [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/email_template.xml',
        'views/equipment_views.xml',
        # 'views/dashboard_views.xml',
        'views/maintenance_team_views.xml',
        'views/maintenance_checklist_views.xml',
        'views/maintenance_categories_views.xml',
        'views/maintenance_schedule_views.xml',
        'views/equipment_spare_parts_views.xml',
        'views/maintenance_request_views.xml',
        'views/equipment_menuitem.xml',
    ],
    "auto_install": False,
    "installable": True,
    "application": False,
}
