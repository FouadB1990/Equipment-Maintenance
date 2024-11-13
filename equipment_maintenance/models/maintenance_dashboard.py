# -*- coding: utf-8 -*-

import ast
from datetime import date, datetime, timedelta
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT


class MaintenanceDashboard(models.Model):
    _name = 'maintenance.dashboard'

    name = fields.Char(string="Test")
    new_request_count = fields.Integer(compute='_compute_counts')
    in_progress_count = fields.Integer(compute='_compute_counts')


    @api.depends('name')
    def _compute_counts(self):
        for record in self:
            record.new_request_count = self.env['sale.order'].search_count([])
            record.in_progress_count = self.env['sale.order'].search_count([])