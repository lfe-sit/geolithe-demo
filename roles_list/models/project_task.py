from odoo import api, models, fields, _
from odoo.exceptions import UserError


class ProjectTask(models.Model):
    _inherit = 'project.task'

    role_ids = fields.Many2many('roles.template.list', 'project_task_roles_rel', 'project_task_id', 'role_id', string="Rôles liés")
