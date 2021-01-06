# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _


class CreateRole(models.TransientModel):
    _name = 'create.role'
    _description = 'Create role'

    date_creation_role = fields.Date('Date', required=True)
