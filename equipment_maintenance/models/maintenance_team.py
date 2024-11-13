from odoo import api, fields, models, _
from odoo.exceptions import UserError


TEAM_STATE = [
    ('draft', "New"),
    ('confirmed', "Ready"),
    ('canceled', "Cancelled"),
    ]

class MaintenanceTeamInherit(models.Model):
    _name = 'maintenance.team'
    _inherit = ['maintenance.team', 'mail.thread', 'mail.activity.mixin']


    state = fields.Selection(
        selection=TEAM_STATE,
        string="Status",
        readonly=True, copy=False, index=True,
        tracking=3,
        default='draft')
    
    team_count = fields.Integer("Members Count", default=3, readonly = True ,
                                compute='_compute_member_count', store = True)

    team_limit = fields.Integer("Members Limit", default=10)




    @api.depends('member_ids')
    def _compute_member_count(self):
        """ Compute the number of members in the team """
        for team in self:
            team.team_count = len(team.member_ids)

    
    # buttons ---------------------------
    
    def button_confirm(self):
        """These method for set the Team in Ready state."""
        for rec in self:
            rec.write({'state': 'confirmed'})

    def button_cancel(self):
        """These method for set the Team in Canceled State."""
        for rec in self:
            rec.write({'state': 'canceled'})