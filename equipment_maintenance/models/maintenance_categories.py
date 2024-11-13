from odoo import api, fields, models, _
from odoo.exceptions import UserError


class MaintenanceChecklist(models.Model):
    _name = "maintenance.categories"
    _description = 'Maintenance Categories'

    name = fields.Char(
        string="category Name.",
        required=True, copy=False, readonly=False)
    
    description = fields.Char(string='Description')

    _sql_constraints = [
                    ('field_unique', 
                    'unique(name)',
                    'Choose another value - it has to be unique!')]