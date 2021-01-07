from odoo import api, models, fields, _
from odoo.exceptions import UserError

import logging

_logger = logging.getLogger(__name__)


class HrEmployee(models.Model):

    _inherit = 'hr.employee'

    def name_get(self):
        if self.name and self.job_title:
            return "{} - {}".format(self.name, self.job_title)
        else:
            result = super(HrEmployee, self).name_get()
        return result