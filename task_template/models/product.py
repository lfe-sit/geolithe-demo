from odoo import models, fields, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    service_tracking = fields.Selection(selection_add=[
        ('task_template_global_project', 'Create a task in an existing project based on task template'),
        ('task_template_new_project', 'Create a task in a new project based on task template'),
    ])
    task_template_ids = fields.Many2many('project.task.template', 'template_product_rel', 'product_id', 'task_template_id', string="Tasks Template")
