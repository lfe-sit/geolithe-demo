from odoo import api, models, fields, _
from odoo.exceptions import UserError


class TaskTemplate(models.Model):
    _name = 'project.task.template'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _mail_post_access = 'read'
    _order = "id desc"
    _description = """Task template object.
                        A task template give the ability to define templates and creates tasks from them
    """

    active = fields.Boolean(default=True)
    name = fields.Char(string='Title', tracking=True, required=True, index=True)
    description = fields.Html(string='Description', tracking=True)
    tag_ids = fields.Many2many('project.tags', string='Tags', tracking=True)
    planned_hours = fields.Float("Planned Hours", help='It is the time planned to achieve the task template. If this task has sub-tasks, it means the time needed to achieve this tasks and its childs.', tracking=True)
    subtask_planned_hours = fields.Float("Subtasks Planned Hours", tracking=True, compute='_compute_subtask_planned_hours', help="Computed using sum of hours planned of all subtasks created from main task. Usually these hours are less or equal to the Planned Hours (of main task).")
    parent_id = fields.Many2one('project.task.template', string='Parent Task', index=True, tracking=True)
    child_ids = fields.One2many('project.task.template', 'parent_id', string="Sub-tasks", context={'active_test': False}, tracking=True)
    product_ids = fields.Many2many('product.template', 'template_product_rel', 'task_template_id', 'product_id', string="Related Articles", tracking=True)
    role_ids = fields.One2many('roles.template.list', 'project_template_id', string="Rôles liés", tracking=True)

    @api.depends('child_ids.planned_hours')
    def _compute_subtask_planned_hours(self):
        for task in self:
            task.subtask_planned_hours = sum(task.child_ids.mapped('planned_hours'))

    def unlink(self):
        for task in self:
            if task.product_ids:
                raise UserError(_("You can't delete an associated task template, Try to delete the link first from all related product and retry again!"))
        return super(TaskTemplate, self).unlink()


