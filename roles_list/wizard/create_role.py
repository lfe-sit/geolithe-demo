# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
import pytz

from odoo import api, fields, models, _
from datetime import date, datetime, timedelta, time
from dateutil import relativedelta 
from math import ceil, modf
from pytz import timezone

_logger = logging.getLogger(__name__)


class CreateRole(models.TransientModel):
    _name = 'create.role'
    _description = 'Create role'

    date_creation_role = fields.Date('Date', required=True)
    project_task_id = fields.Many2one('project.task', required=True)
    
    def _getstart_datetime(self, date,  start_time):
        h = int(start_time)
        m = round(modf(start_time)[0] * 60.0)

        start = datetime.combine(date, time(h, m))
        start_datetime = start.astimezone(pytz.utc).replace(tzinfo=None)
        return start_datetime

    def _getend_datetime(self, date, duration, start_time):
        start_time = self._getstart_datetime(date, start_time)

        h, m = divmod(duration, 1)
        delta = timedelta(hours=int(h), minutes=int(m * 60))
        end_datetime = start_time + delta
        return end_datetime
        
    def validate_create_role(self):
        self.ensure_one()
        values = []
        for r in self.project_task_id.role_ids:          
            for n in range(r.number):
                _logger.info(r.role.role_id.name)
                _logger.info(n)

                values.append({'role_id': r.role.role_id.id, 
                             'project_id': self.project_task_id.project_id.id, 
                             'task_id': self.project_task_id.id,
                             'start_datetime': self._getstart_datetime(self.date_creation_role, r.role.start_time),
                             'end_datetime': self._getend_datetime(self.date_creation_role, r.role.duration, r.role.start_time),
                             'template_id': r.role.id
                            })
                _logger.info(values)

        res = self.env['planning.slot'].create(values)
 
        return {'type': 'ir.actions.act_window_close'}