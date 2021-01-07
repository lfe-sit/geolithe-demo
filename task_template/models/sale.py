from odoo import api, models, _


class OrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _timesheet_create_task_template_prepare_values(self, project, task_temp, vals, parent):
        self.ensure_one()
        vals.update({
            'name': task_temp.name,
            'planned_hours': task_temp.planned_hours,
            'partner_id': self.order_id.partner_id.id,
            'description': task_temp.description,
            'project_id': project.id,
            'sale_line_id': self.id,
            'tag_ids': [(6, 0, task_temp.tag_ids.ids)],
            'company_id': self.company_id.id,
            'parent_id': parent.id if parent else None,
            'user_id': False,  # force non assigned task, as created as sudo()
        })
        return vals

    def _timesheet_create_task_template(self, project, task_temp, parent):
        """ Generate task for the given so line based on template, and link it.
            :param project: record of project.project in which the task should be created
                   task_temp: record of a template task
                   parent: for the creation of parent task
            :return task: record of the created task
        """
        vals = {}
        values = self._timesheet_create_task_template_prepare_values(project, task_temp, vals, parent)
        task = self.env['project.task'].sudo().create(values)
        self.write({'task_id': task.id})
        # post message on task
        task_msg = _("This task has been created from: <a href=# data-oe-model=sale.order data-oe-id=%d>%s</a> (%s)") % (self.order_id.id, self.order_id.name, self.product_id.name)
        task.message_post(body=task_msg)

        # Retirer odooBot from abonnées
        id_odoo_bot = self.env.ref('base.partner_root')
        partners = []
        for part in id_odoo_bot:
            partners.append(part.id)
        task.message_unsubscribe(partner_ids=partners, channel_ids=None)
        return task

    def _timesheet_create_task(self, project):
        record = super(OrderLine, self)._timesheet_create_task(project)
        # Retirer odooBot from abonnées
        id_odoo_bot = self.env.ref('base.partner_root')
        partners = []
        for part in id_odoo_bot:
            partners.append(part.id)
        record.message_unsubscribe(partner_ids=partners, channel_ids=None)
        return record

    def _timesheet_service_generation(self):
        """ Override Standard function by adding the two specific option of creation tasks based on template"""
        # Override the original _timesheet_service_generation function
        record = super(OrderLine, self)._timesheet_service_generation()
        ########################################################################################
        # Alert Attention
        # This is a copy code of original function of odoo
        # It is necessery to verify this function after every pull
        # The original function is located in sale_timesheet addons, at the file sale_order.py
        ########################################################################################
        so_line_task_global_project_task_template = self.filtered(lambda sol: sol.is_service and sol.product_id.service_tracking == 'task_template_global_project')
        so_line_new_project_task_template = self.filtered(lambda sol: sol.is_service and sol.product_id.service_tracking in ['task_template_new_project'])
        so_line_new_project = self.filtered(lambda sol: sol.is_service and sol.product_id.service_tracking in ['project_only', 'task_new_project'])
        # search so lines from SO of current so lines having their project generated, in order to check if the current one can
        # create its own project, or reuse the one of its order.
        map_so_project_task_template = {}
        if so_line_new_project_task_template:
            order_ids_task_template = self.mapped('order_id').ids
            so_lines_with_project_task_template = self.search([('order_id', 'in', order_ids_task_template), ('project_id', '!=', False), ('product_id.service_tracking', 'in', ['task_template_new_project']), ('product_id.project_template_id', '=', False)])
            map_so_project_task_template = {sol.order_id.id: sol.project_id for sol in so_lines_with_project_task_template}
            so_lines_with_project_templates_task_template = self.search([('order_id', 'in', order_ids_task_template), ('project_id', '!=', False), ('product_id.service_tracking', 'in', ['task_template_new_project']), ('product_id.project_template_id', '!=', False)])
            map_so_project_templates_task_template = {(sol.order_id.id, sol.product_id.project_template_id.id): sol.project_id for sol in so_lines_with_project_templates_task_template}

        # search the global project of current SO lines, in which create their task
        map_sol_project_task_template = {}
        if so_line_task_global_project_task_template:
            map_sol_project_task_template = {sol.id: sol.product_id.with_context(force_company=sol.company_id.id).project_id for sol in so_line_task_global_project_task_template}

        def _can_create_project_task_template(sol):
            if not sol.project_id:
                if sol.product_id.project_template_id:
                    return (sol.order_id.id, sol.product_id.project_template_id.id) not in map_so_project_templates_task_template
                elif sol.order_id.id not in map_so_project_task_template:
                    return True
            return False

        # task_global_project: create task in global project
        for so_line in so_line_task_global_project_task_template:
            if not so_line.task_id:
                if map_sol_project_task_template.get(so_line.id):
                    for task_temp in so_line.product_id.task_template_ids:
                        parent_task = so_line._timesheet_create_task_template(project=map_sol_project_task_template[so_line.id], task_temp=task_temp, parent=None)
                        # Create a sub tasks
                        for sub_task_tmp in task_temp.child_ids:
                            if sub_task_tmp:
                                so_line._timesheet_create_task_template(project=map_sol_project_task_template[so_line.id], task_temp=sub_task_tmp, parent=parent_task)

        # project_only, task_new_project: create a new project, based or not on a template (1 per SO). May be create a task too.
        for so_line in so_line_new_project_task_template:
            # Test if Odoo has create a project in standard function
            if so_line_new_project:
                for line in so_line_new_project:
                    project = line.project_id
            else:
                project = so_line.project_id
            if not project and _can_create_project_task_template(so_line):
                project = so_line._timesheet_create_project()
                if so_line.product_id.project_template_id:
                    map_so_project_templates_task_template[(so_line.order_id.id, so_line.product_id.project_template_id.id)] = project
                else:
                    map_so_project_task_template[so_line.order_id.id] = project
            if so_line.product_id.service_tracking == 'task_template_new_project':
                if not project:
                    if so_line.product_id.project_template_id:
                        project = map_so_project_templates_task_template[(so_line.order_id.id, so_line.product_id.project_template_id.id)]
                    else:
                        project = map_so_project_task_template[so_line.order_id.id]
                if not so_line.task_id:
                    for task_temp in so_line.product_id.task_template_ids:
                        parent_task = so_line._timesheet_create_task_template(project=project, task_temp=task_temp, parent=None)
                        # Create a sub tasks
                        if task_temp.child_ids:
                            for sub_task_tmp in task_temp.child_ids:
                                so_line._timesheet_create_task_template(project=project, task_temp=sub_task_tmp, parent=parent_task)
        return record
