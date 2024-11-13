from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

class MaintenanceRequestOrderLine(models.Model):
    _name = 'maintenance.request.order.line'
    _description = 'Maintenance Request Order Line'

    maintenance_request_order_id = fields.Many2one('maintenance.request.order', string='Maintenance Request', required=True, ondelete='cascade')

    spare_part_id = fields.Many2one('equipment.spare.parts', string='Spare Part', required=True)

    quantity = fields.Float(string='Quantity', default=1.0)
    cost = fields.Float(string='Cost', related='spare_part_id.cost')
    description = fields.Text(string='Description')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
    ], default='draft')

