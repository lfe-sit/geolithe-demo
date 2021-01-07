from odoo import api, models, fields, _
from odoo.exceptions import UserError

import logging

_logger = logging.getLogger(__name__)

class PlanningRole(models.Model):
    _inherit = 'planning.role'

    equipment = fields.Many2one('maintenance.equipment')

class PlanningRoleTemplate(models.Model):
    _inherit = 'planning.slot.template'

    equipment = fields.Many2one('maintenance.equipment')

class PlanningSLot(models.Model):
    _inherit = 'planning.slot'

    equipment = fields.Many2one('maintenance.equipment')