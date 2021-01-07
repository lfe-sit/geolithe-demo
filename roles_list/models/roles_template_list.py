from odoo import api, models, fields, _
from odoo.exceptions import UserError


class RolesTemplateList(models.Model):
    _name = 'roles.template.list'
    _order = "id desc"
    _description = """Roles template list
    """

    role = fields.Many2one('planning.slot.template', "Poste souhaité")
    equipment = fields.Many2one('maintenance.equipment')
    number = fields.Integer("Nombre de poste")
    project_template_id = fields.Many2one('project.task.template')