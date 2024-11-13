from odoo import api, fields, models, _
from odoo.exceptions import UserError


class EquipmentSpareParts(models.Model):
    _name = "equipment.spare.parts"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Equipment Spare Parts'


    name = fields.Char('Equipment Name', required=True, translate=True)
    company_id = fields.Many2one('res.company', string='Company',
        default=lambda self: self.env.company)
    active = fields.Boolean(default=True)
    category_id = fields.Many2one('maintenance.equipment.category', string='Equipment Category',
                                  tracking=True, group_expand='_read_group_category_ids')
    partner_id = fields.Many2one('res.partner', string='Vendor', check_company=True)
    partner_ref = fields.Char('Vendor Reference')
    location = fields.Char('Location')
    model = fields.Char('Model')
    serial_no = fields.Char('Serial Number', copy=False)
    assign_date = fields.Date('Assigned Date', tracking=True)
    effective_date = fields.Date('Effective Date', default=fields.Date.context_today, required=True, help="Date at which the equipment became effective. This date will be used to compute the Mean Time Between Failure.")
    cost = fields.Float('Cost')
    note = fields.Html('Note')
    warranty_date = fields.Date('Warranty Expiration Date')
    color = fields.Integer('Color Index')
    scrap_date = fields.Date('Scrap Date')
    maintenance_ids = fields.One2many('maintenance.request', 'equipment_id')
    maintenance_count = fields.Integer(compute='_compute_maintenance_count', string="Maintenance Count", store=True)
    maintenance_open_count = fields.Integer(compute='_compute_maintenance_count', string="Current Maintenance", store=True)
    maintenance_team_id = fields.Many2one('maintenance.team', string='Maintenance Team', check_company=True)

    related_machines_ids = fields.Many2many("maintenance.equipment", string="Related Machines", check_company=True)

    maintenance_request_order_id = fields.Many2one('maintenance.request.order', string='Maintenance Request', ondelete='cascade')


    def name_get(self):
        result = []
        for record in self:
            if record.name and record.serial_no:
                result.append((record.id, record.name + '/' + record.serial_no))
            if record.name and not record.serial_no:
                result.append((record.id, record.name))
        return result