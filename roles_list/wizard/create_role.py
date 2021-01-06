# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _


class CreateRole(models.TransientModel):
    _name = 'create.role'
    _description = 'Create role'

    date_creation_role = fields.Date('Date', required=True)
    role_ids = fields.Many2many('roles.template.list', 'project_task_create_roles_rel', 'project_task_id', 'role_id', string="Rôles liés")
    
    def validate_create_role(self):
        self.ensure_one()
        self.user_ids.action_apply()
        return {'type': 'ir.actions.act_window_close'}