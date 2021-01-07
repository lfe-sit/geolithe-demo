from odoo import api, models, fields, _
from odoo.exceptions import UserError

import logging

_logger = logging.getLogger(__name__)

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
            'context': dict(self.env.context,  
                            default_project_task_id=self.id),
        }
