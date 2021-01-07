from odoo import api, models, fields, _
from odoo.exceptions import UserError

import logging

_logger = logging.getLogger(__name__)


class HrEmployee(models.Model):

    _inherit = 'hr.employee'

    def name_get(self):
        res = dict(super(HrEmployee, self).name_get())
        for e in self:
            if e.name and e.job_title:
                res[e.id] = "{} - {}".format(e.name, e.job_title)
        return list(res.items())
    