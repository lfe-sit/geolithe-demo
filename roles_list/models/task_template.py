from odoo import api, models, fields, _
from odoo.exceptions import UserError


class TaskTemplate(models.Model):
    _inherit = 'project.task.template'

    role_ids = fields.One2many('roles.template.list', 'project_template_id', string="Rôles liés", tracking=True)
