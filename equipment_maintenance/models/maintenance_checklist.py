from odoo import api, fields, models, _
from odoo.exceptions import UserError


class MaintenanceChecklist(models.Model):
    _name = "maintenance.checklist"
    _description = 'Maintenance Checklist'

    name = fields.Char(
        string="Checklist Name.",
        required=True, copy=False, readonly=False)
    
    description = fields.Char(string='Description')

    _sql_constraints = [
                    ('field_unique', 
                    'unique(name)',
                    'Choose another value - it has to be unique!')]