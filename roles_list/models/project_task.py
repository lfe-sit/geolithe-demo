from odoo import api, models, fields, _
from odoo.exceptions import UserError


class ProjectTask(models.Model):
    _inherit = 'project.task'

    role_ids = fields.Many2many('roles.template.list', 'project_task_roles_rel', 'project_task_id', 'role_id', string="Rôles liés")
    
    def create_role_action(self):
        view = self.env.ref('roles_list.create_role_wizard')
        return {
            'name': _('Créer les postes'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'create.role',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': dict(self.env.context,  default_role_ids==[(0, 0, {'role':  p.role, 'number': p.number, project_template_id: p.project_template_id}) 
                                                                  for p in self.role_ids]),
        }
