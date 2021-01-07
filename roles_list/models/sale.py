from odoo import api, models, _


class OrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _timesheet_create_task_template_prepare_values(self, project, task_temp, vals, parent):
        super(OrderLine, self)._timesheet_create_task_template_prepare_values(project, task_temp, vals, parent)
        self.ensure_one()
        vals.update({
            'role_ids': [(6, 0, task_temp.role_ids.ids)]
        })

        return vals