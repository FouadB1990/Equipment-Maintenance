from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime, timedelta


SCHEDULE_STATE = [
    ('draft', "New"),
    ('confirmed', "Confirmed"),
    ('canceled', "Cancelled"),
    ]

class MaintenanceSchedule(models.Model):
    _name = "maintenance.schedule"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "id DESC"
    _description = 'Maintenance Schedule'

    
    name = fields.Char(
        string="Schedule No.",
        required=True, copy=False, readonly=False,
        index='trigram',
        default=lambda self: _('New'))
    
    state = fields.Selection(
        selection=SCHEDULE_STATE,
        string="Status",
        readonly=True, copy=False, index=True,
        tracking=3,
        default='draft')
    
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    
    active = fields.Boolean(default=True)
    
    technician_user_id = fields.Many2one('res.users', string='Responsible', tracking=True)

    machine_id = fields.Many2one("maintenance.equipment", string = "Machines", required = True, check_company=True)

    category_id = fields.Many2one('maintenance.equipment.category', string='Equipment Category',
                                  tracking=True, group_expand='_read_group_category_ids')
    
    model = fields.Char('Model')

    serial_no = fields.Char('Serial Number', copy=False)
    
    warranty_date = fields.Date('Warranty Expiration Date')

    cost = fields.Float('Cost')

    maintenance_expected_date = fields.Date('Maintenance Expected Date')

    



    
    
    description = fields.Char(string='Description')

    # buttons ---------------------------
    
    def button_confirm(self):
        """These method for set the Schedule Order in Confirmed state."""
        for rec in self:
            rec.write({'state': 'confirmed'})

    def button_cancel(self):
        """These method for set the Team in Canceled State."""
        for rec in self:
            rec.write({'state': 'canceled'})

    
    @api.ondelete(at_uninstall=False)
    def _unlink_except_cancel(self):
        for order in self:
            if order.state not in ('draft', 'canceled'):
                raise UserError(_(
                    "You Can Not Delete a Confirmed Schedule ."
                    " You must First Cancel it."))


    

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('maintenance.schedule')

            return super().create(vals_list)
    


    @api.onchange('machine_id')
    def _onchange_machine_id(self):
        if self.machine_id:
            self.category_id = self.machine_id.category_id.id if self.machine_id.category_id else False
            self.model = self.machine_id.model
            self.serial_no = self.machine_id.serial_no
            self.warranty_date = self.machine_id.warranty_date
            self.cost = self.machine_id.cost

    # Send notify Email
    @api.model
    def send_maintenance_reminder(self):
        """Send a reminder email to users about upcoming maintenance"""
        today = fields.Date.today() 
        one_week_later = (datetime.datetime.strptime(today, DEFAULT_SERVER_DATE_FORMAT) + datetime.timedelta(weeks=1)).date()

        schedules_to_notify = self.search([
            ('maintenance_expected_date', '=', one_week_later),
            ('technician_user_id', '!=', False),
        ])

        for schedule in schedules_to_notify:
            if schedule.technician_user_id:
                template = self.env.ref('equipment_maintenance.maintenance_schedule_reminder_template')
                template.sudo().send_mail(schedule.id, force_send=True)

    
    